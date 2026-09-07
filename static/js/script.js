/**
 * AI Content Studio - Clean Client Script
 * Handles theme switching (Dark/Light with localStorage),
 * single-page continuous flow generation, Markdown rendering,
 * clipboard copy, and file download.
 */

document.addEventListener("DOMContentLoaded", () => {
    // =========================================================================
    // 1. Theme Management (Dark Velvet Maroon / Light Rose-White with localStorage)
    // =========================================================================
    const themeToggleBtn = document.getElementById("themeToggleBtn");
    const THEME_STORAGE_KEY = "ai_content_studio_theme";

    function getSavedTheme() {
        const saved = localStorage.getItem(THEME_STORAGE_KEY);
        if (saved === "light" || saved === "dark") {
            return saved;
        }
        return "dark"; // Default to dark velvet maroon
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem(THEME_STORAGE_KEY, theme);
    }

    applyTheme(getSavedTheme());

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", () => {
            const current = document.documentElement.getAttribute("data-theme") || "dark";
            const nextTheme = current === "dark" ? "light" : "dark";
            applyTheme(nextTheme);
            showToast(`Switched to ${nextTheme === "dark" ? "Dark" : "Light"} mode`);
        });
    }

    // =========================================================================
    // 2. DOM Elements
    // =========================================================================
    const form = document.getElementById("generatorForm");
    const generateBtn = document.getElementById("generateBtn");
    const btnText = generateBtn.querySelector(".btn-text");
    const btnIcon = generateBtn.querySelector(".btn-icon");
    const btnSpinner = generateBtn.querySelector(".btn-spinner");

    const contentTypeSelect = document.getElementById("contentTypeSelect");
    const topicInput = document.getElementById("topicInput");
    const topicCharCount = document.getElementById("topicCharCount");
    const audienceSelect = document.getElementById("audienceSelect");
    const customAudienceInput = document.getElementById("customAudienceInput");
    const toneSelect = document.getElementById("toneSelect");
    const lengthSelect = document.getElementById("lengthSelect");
    const styleSelect = document.getElementById("styleSelect");
    const instructionsInput = document.getElementById("instructionsInput");

    // Output Views & Actions (Continuous vertical flow)
    const loadingState = document.getElementById("loadingState");
    const outputDivider = document.getElementById("outputDivider");
    const outputSection = document.getElementById("outputSection");
    const outputSubtitle = document.getElementById("outputSubtitle");
    const contentPreview = document.getElementById("contentPreview");
    const markdownOutput = document.getElementById("markdownOutput");

    const copyBtn = document.getElementById("copyBtn");
    const copyBtnText = document.getElementById("copyBtnText");
    const regenerateBtn = document.getElementById("regenerateBtn");
    const downloadBtn = document.getElementById("downloadBtn");
    const clearBtn = document.getElementById("clearBtn");

    const metricsBar = document.getElementById("metricsBar");
    const wordCountBadge = document.getElementById("wordCountBadge");
    const charCountBadge = document.getElementById("charCountBadge");
    const typeBadge = document.getElementById("typeBadge");

    // Alert & Toast Elements
    const globalAlert = document.getElementById("globalAlert");
    const globalAlertMessage = document.getElementById("globalAlertMessage");
    const alertCloseBtn = document.getElementById("alertCloseBtn");
    const toastMessage = document.getElementById("toastMessage");
    const toastText = document.getElementById("toastText");

    let currentRawContent = "";
    let lastGeneratedParams = null;
    let toastTimeout = null;

    if (window.marked) {
        marked.setOptions({ breaks: true, gfm: true });
    }

    // =========================================================================
    // 3. Topic Character Count Live Update
    // =========================================================================
    topicInput.addEventListener("input", () => {
        const count = topicInput.value.length;
        topicCharCount.textContent = `${count} character${count === 1 ? "" : "s"}`;
    });

    // =========================================================================
    // 4. Example Topic Chips Click Handling
    // =========================================================================
    const exampleTags = document.querySelectorAll(".example-tag");
    exampleTags.forEach(tag => {
        tag.addEventListener("click", () => {
            const topic = tag.getAttribute("data-topic");
            if (topic) {
                topicInput.value = topic;
                topicInput.dispatchEvent(new Event("input"));
                topicInput.focus();
                showToast(`Inserted "${topic}"`);
            }
        });
    });

    // =========================================================================
    // 5. Custom Audience Field Toggle
    // =========================================================================
    audienceSelect.addEventListener("change", () => {
        if (audienceSelect.value === "Custom") {
            customAudienceInput.style.display = "block";
            customAudienceInput.focus();
        } else {
            customAudienceInput.style.display = "none";
        }
    });

    // =========================================================================
    // 6. Helpers: Alert, Toast, Metrics
    // =========================================================================
    function showAlert(message) {
        globalAlertMessage.textContent = message;
        globalAlert.style.display = "flex";
        globalAlert.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function hideAlert() {
        globalAlert.style.display = "none";
        globalAlertMessage.textContent = "";
    }

    alertCloseBtn.addEventListener("click", hideAlert);

    function showToast(text) {
        if (toastTimeout) clearTimeout(toastTimeout);
        toastText.textContent = text;
        toastMessage.style.display = "flex";
        toastTimeout = setTimeout(() => {
            toastMessage.style.display = "none";
        }, 2600);
    }

    function updateMetrics(text, type) {
        const trimmed = text.trim();
        const words = trimmed ? trimmed.split(/\s+/).length : 0;
        const chars = text.length;

        wordCountBadge.textContent = words.toLocaleString();
        charCountBadge.textContent = chars.toLocaleString();
        typeBadge.textContent = type || contentTypeSelect.value;
    }

    function setLoading(isLoading) {
        if (isLoading) {
            generateBtn.disabled = true;
            btnText.textContent = "Creating your content...";
            btnSpinner.style.display = "inline-block";
            btnIcon.style.display = "none";

            loadingState.style.display = "flex";
            loadingState.scrollIntoView({ behavior: "smooth", block: "nearest" });
        } else {
            generateBtn.disabled = false;
            btnText.textContent = "Generate Content";
            btnSpinner.style.display = "none";
            btnIcon.style.display = "inline-flex";
            loadingState.style.display = "none";
        }
    }

    // =========================================================================
    // 7. Generation Logic (POST /generate)
    // =========================================================================
    async function handleGenerate(customPayload = null) {
        hideAlert();

        const topic = (customPayload ? customPayload.topic : topicInput.value).trim();
        if (!topic) {
            showAlert("Please enter a topic before generating content.");
            topicInput.focus();
            return;
        }

        let resolvedAudience = customPayload ? customPayload.audience : audienceSelect.value;
        if (resolvedAudience === "Custom") {
            const customVal = customAudienceInput.value.trim();
            resolvedAudience = customVal || "General Audience";
        }

        const payload = customPayload || {
            content_type: contentTypeSelect.value,
            topic: topic,
            audience: resolvedAudience,
            tone: toneSelect.value,
            length: lengthSelect.value,
            style: styleSelect.value,
            additional_instructions: instructionsInput.value.trim(),
        };

        lastGeneratedParams = payload;
        setLoading(true);

        try {
            const response = await fetch("/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                const errorMsg = data.error || "Unable to generate content right now. Please check your API configuration.";
                showAlert(errorMsg);
                return;
            }

            currentRawContent = data.content;

            if (window.marked) {
                markdownOutput.innerHTML = marked.parse(currentRawContent);
            } else {
                markdownOutput.textContent = currentRawContent;
            }

            updateMetrics(currentRawContent, data.content_type || payload.content_type);

            outputDivider.style.display = "block";
            outputSection.style.display = "flex";
            outputSubtitle.textContent = `Generated for ${payload.audience} • ${payload.tone} tone`;

            setTimeout(() => {
                outputSection.scrollIntoView({ behavior: "smooth", block: "start" });
            }, 50);

            showToast("Content generated successfully!");

        } catch (error) {
            console.error("Generation Error:", error);
            showAlert("Failed to connect to the server. Please verify the Flask backend is running.");
        } finally {
            setLoading(false);
        }
    }

    generateBtn.addEventListener("click", () => handleGenerate());

    // =========================================================================
    // 8. Toolbar Actions (Copy, Regenerate, Download, Clear)
    // =========================================================================
    copyBtn.addEventListener("click", async () => {
        if (!currentRawContent) return;

        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                await navigator.clipboard.writeText(currentRawContent);
            } else {
                const dummy = document.createElement("textarea");
                dummy.value = currentRawContent;
                document.body.appendChild(dummy);
                dummy.select();
                document.execCommand("copy");
                document.body.removeChild(dummy);
            }

            copyBtnText.textContent = "Copied!";
            copyBtn.style.color = "var(--accent-success)";
            showToast("Copied to clipboard!");

            setTimeout(() => {
                copyBtnText.textContent = "Copy";
                copyBtn.style.color = "";
            }, 2000);
        } catch (err) {
            console.error("Clipboard copy error:", err);
            showAlert("Could not copy automatically. Please select text and copy manually.");
        }
    });

    regenerateBtn.addEventListener("click", () => {
        if (lastGeneratedParams) {
            handleGenerate(lastGeneratedParams);
        } else {
            handleGenerate();
        }
    });

    downloadBtn.addEventListener("click", () => {
        if (!currentRawContent) return;

        const blob = new Blob([currentRawContent], { type: "text/plain;charset=utf-8" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");

        const typeSlug = (contentTypeSelect.value || "generated_content")
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, "_");

        a.href = url;
        a.download = `${typeSlug}_${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        showToast("File downloaded!");
    });

    clearBtn.addEventListener("click", () => {
        currentRawContent = "";
        lastGeneratedParams = null;
        markdownOutput.innerHTML = "";
        outputSection.style.display = "none";
        outputDivider.style.display = "none";

        showToast("Output cleared");
    });

    // =========================================================================
    // 10. Custom Dropdowns Initialization (Guaranteed Light Blue Hover Everywhere)
    // =========================================================================
    function initCustomSelects() {
        const wrappers = document.querySelectorAll(".select-wrapper");
        wrappers.forEach(wrapper => {
            const select = wrapper.querySelector("select.form-select");
            if (!select) return;

            wrapper.classList.add("custom-active");

            // Create Trigger
            const trigger = document.createElement("div");
            trigger.className = "custom-select-trigger";
            trigger.tabIndex = 0;
            trigger.setAttribute("role", "combobox");
            trigger.setAttribute("aria-expanded", "false");
            trigger.setAttribute("aria-label", select.getAttribute("aria-label") || select.name || "Select option");

            const valueSpan = document.createElement("span");
            valueSpan.className = "custom-select-value";
            const selectedOpt = select.options[select.selectedIndex] || select.options[0];
            valueSpan.textContent = selectedOpt ? selectedOpt.text : "";

            const arrowSpan = document.createElement("span");
            arrowSpan.className = "custom-select-arrow";
            arrowSpan.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>`;

            trigger.appendChild(valueSpan);
            trigger.appendChild(arrowSpan);

            // Create Dropdown Menu
            const dropdown = document.createElement("div");
            dropdown.className = "custom-select-dropdown";
            dropdown.setAttribute("role", "listbox");

            function populateOptions() {
                dropdown.innerHTML = "";
                Array.from(select.options).forEach((opt, idx) => {
                    const optEl = document.createElement("div");
                    optEl.className = "custom-select-option";
                    if (opt.selected) optEl.classList.add("is-selected");
                    optEl.setAttribute("data-value", opt.value);
                    optEl.setAttribute("data-index", idx);
                    optEl.setAttribute("role", "option");

                    const textSpan = document.createElement("span");
                    textSpan.textContent = opt.text;

                    const checkSpan = document.createElement("span");
                    checkSpan.className = "custom-select-check";
                    checkSpan.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;

                    optEl.appendChild(textSpan);
                    optEl.appendChild(checkSpan);

                    optEl.addEventListener("click", (e) => {
                        e.stopPropagation();
                        selectOption(opt.value, opt.text);
                        closeDropdown();
                    });

                    dropdown.appendChild(optEl);
                });
            }

            populateOptions();

            function selectOption(val, text) {
                select.value = val;
                valueSpan.textContent = text;

                dropdown.querySelectorAll(".custom-select-option").forEach(el => {
                    if (el.getAttribute("data-value") === val) {
                        el.classList.add("is-selected");
                    } else {
                        el.classList.remove("is-selected");
                    }
                });

                select.dispatchEvent(new Event("change", { bubbles: true }));
            }

            function openDropdown() {
                document.querySelectorAll(".select-wrapper.open").forEach(w => {
                    if (w !== wrapper) {
                        w.classList.remove("open");
                        const trig = w.querySelector(".custom-select-trigger");
                        if (trig) trig.setAttribute("aria-expanded", "false");
                    }
                });

                wrapper.classList.add("open");
                trigger.setAttribute("aria-expanded", "true");

                const selEl = dropdown.querySelector(".is-selected");
                if (selEl) {
                    selEl.scrollIntoView({ block: "nearest" });
                }
            }

            function closeDropdown() {
                wrapper.classList.remove("open");
                trigger.setAttribute("aria-expanded", "false");
                dropdown.querySelectorAll(".custom-select-option").forEach(el => el.classList.remove("is-highlighted"));
            }

            trigger.addEventListener("click", (e) => {
                e.stopPropagation();
                if (wrapper.classList.contains("open")) {
                    closeDropdown();
                } else {
                    openDropdown();
                }
            });

            // Keyboard navigation
            trigger.addEventListener("keydown", (e) => {
                if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    if (wrapper.classList.contains("open")) {
                        const highlighted = dropdown.querySelector(".custom-select-option.is-highlighted");
                        if (highlighted) {
                            selectOption(highlighted.getAttribute("data-value"), highlighted.querySelector("span").textContent);
                        }
                        closeDropdown();
                    } else {
                        openDropdown();
                    }
                } else if (e.key === "ArrowDown" || e.key === "ArrowUp") {
                    e.preventDefault();
                    if (!wrapper.classList.contains("open")) {
                        openDropdown();
                    }
                    const options = Array.from(dropdown.querySelectorAll(".custom-select-option"));
                    const currentIndex = options.findIndex(el => el.classList.contains("is-highlighted") || el.classList.contains("is-selected"));
                    let nextIndex = e.key === "ArrowDown" ? currentIndex + 1 : currentIndex - 1;
                    if (nextIndex >= options.length) nextIndex = 0;
                    if (nextIndex < 0) nextIndex = options.length - 1;

                    options.forEach(el => el.classList.remove("is-highlighted"));
                    options[nextIndex].classList.add("is-highlighted");
                    options[nextIndex].scrollIntoView({ block: "nearest" });
                } else if (e.key === "Escape" || e.key === "Tab") {
                    closeDropdown();
                }
            });

            // Sync with native select if changed elsewhere
            select.addEventListener("change", () => {
                const currentOpt = select.options[select.selectedIndex];
                if (currentOpt) {
                    valueSpan.textContent = currentOpt.text;
                    dropdown.querySelectorAll(".custom-select-option").forEach(el => {
                        el.classList.toggle("is-selected", el.getAttribute("data-value") === currentOpt.value);
                    });
                }
            });

            wrapper.appendChild(trigger);
            wrapper.appendChild(dropdown);
        });

        // Close on click outside
        document.addEventListener("click", (e) => {
            if (!e.target.closest(".select-wrapper")) {
                document.querySelectorAll(".select-wrapper.open").forEach(w => {
                    w.classList.remove("open");
                    const trig = w.querySelector(".custom-select-trigger");
                    if (trig) trig.setAttribute("aria-expanded", "false");
                });
            }
        });
    }

    initCustomSelects();
});
