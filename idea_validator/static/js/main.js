document.addEventListener('DOMContentLoaded', () => {
    
    // ==========================================
    // 1. Industry Dropdown "Other" Toggle
    // ==========================================
    const industrySelect = document.getElementById('id_industry');
    const customIndustryInput = document.getElementById('id_custom_industry');
    
    if (industrySelect && customIndustryInput) {
        const toggleCustomIndustry = () => {
            if (industrySelect.value === 'Other') {
                customIndustryInput.classList.remove('hidden');
                customIndustryInput.setAttribute('required', 'required');
            } else {
                customIndustryInput.classList.add('hidden');
                customIndustryInput.removeAttribute('required');
            }
        };
        
        // Run on page load and on change
        toggleCustomIndustry();
        industrySelect.addEventListener('change', toggleCustomIndustry);
    }

    // ==========================================
    // 2. Loading Overlay Text Cycling
    // ==========================================
    const validateForm = document.getElementById('validator-form');
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingStatusText = document.getElementById('loading-status-text');
    
    const loadingPhrases = [
        "Analyzing startup feasibility...",
        "Identifying direct and indirect competitors...",
        "Evaluating SWOT vectors (Strengths, Weaknesses, Opportunities, Threats)...",
        "Structuring the Business Model Canvas...",
        "Synthesizing Go-to-Market channels...",
        "Formulating pricing and monetization structures...",
        "Evaluating risk vectors and mitigations...",
        "Drafting investor pitch presentation slides...",
        "Polishing financial margin estimations..."
    ];
    
    if (validateForm && loadingOverlay && loadingStatusText) {
        validateForm.addEventListener('submit', () => {
            loadingOverlay.classList.remove('hidden');
            let phraseIndex = 0;
            
            setInterval(() => {
                phraseIndex = (phraseIndex + 1) % loadingPhrases.length;
                loadingStatusText.style.opacity = 0;
                setTimeout(() => {
                    loadingStatusText.textContent = loadingPhrases[phraseIndex];
                    loadingStatusText.style.opacity = 1;
                }, 300);
            }, 2500);
        });
    }

    // ==========================================
    // 3. Tab Switching Navigation
    // ==========================================
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-content');
    
    if (tabButtons.length > 0 && tabPanels.length > 0) {
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTabId = button.getAttribute('data-tab');
                
                // Deactivate all buttons
                tabButtons.forEach(btn => btn.classList.remove('active'));
                // Hide all panels
                tabPanels.forEach(panel => panel.classList.add('hidden'));
                
                // Activate clicked button
                button.classList.add('active');
                // Show target panel
                document.getElementById(targetTabId).classList.remove('hidden');
            });
        });
    }

    // ==========================================
    // 4. Investor Pitch Slide Deck
    // ==========================================
    const slides = document.querySelectorAll('.pitch-slide');
    const prevBtn = document.getElementById('prev-slide');
    const nextBtn = document.getElementById('next-slide');
    const dotsContainer = document.getElementById('pitch-dots');
    
    if (slides.length > 0) {
        let currentSlide = 0;
        
        // Generate dots
        slides.forEach((_, index) => {
            const dot = document.createElement('div');
            dot.classList.add('pitch-dot');
            if (index === 0) dot.classList.add('active');
            dot.addEventListener('click', () => showSlide(index));
            dotsContainer.appendChild(dot);
        });
        
        const dots = document.querySelectorAll('.pitch-dot');
        
        const showSlide = (index) => {
            slides[currentSlide].classList.remove('active');
            dots[currentSlide].classList.remove('active');
            
            currentSlide = index;
            
            slides[currentSlide].classList.add('active');
            dots[currentSlide].classList.add('active');
            
            // Disable/enable controls
            if (prevBtn) prevBtn.disabled = currentSlide === 0;
            if (nextBtn) nextBtn.disabled = currentSlide === slides.length - 1;
        };
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                if (currentSlide > 0) {
                    showSlide(currentSlide - 1);
                }
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                if (currentSlide < slides.length - 1) {
                    showSlide(currentSlide + 1);
                }
            });
        }
        
        // Initialize state
        showSlide(0);
    }
    
    // ==========================================
    // 5. Copy Investor Pitch Details
    // ==========================================
    const copyPitchBtn = document.getElementById('copy-pitch-btn');
    if (copyPitchBtn) {
        copyPitchBtn.addEventListener('click', () => {
            const hook = document.querySelector('[data-pitch="hook"]')?.textContent || "";
            const problem = document.querySelector('[data-pitch="problem"]')?.textContent || "";
            const solution = document.querySelector('[data-pitch="solution"]')?.textContent || "";
            const marketSize = document.querySelector('[data-pitch="market"]')?.textContent || "";
            const projections = document.querySelector('[data-pitch="projections"]')?.textContent || "";
            const ask = document.querySelector('[data-pitch="ask"]')?.textContent || "";
            
            const fullText = `STARTUP INVESTOR PITCH DECK\n\n` +
                `1. THE HOOK\n${hook}\n\n` +
                `2. THE PROBLEM\n${problem}\n\n` +
                `3. THE SOLUTION\n${solution}\n\n` +
                `4. MARKET OPPORTUNITY\n${marketSize}\n\n` +
                `5. FINANCIAL PROJECTIONS\n${projections}\n\n` +
                `6. THE ASK\n${ask}`;
                
            navigator.clipboard.writeText(fullText).then(() => {
                const originalText = copyPitchBtn.innerHTML;
                copyPitchBtn.innerHTML = `<i class="fas fa-check"></i> Copied!`;
                copyPitchBtn.style.background = "var(--teal)";
                
                setTimeout(() => {
                    copyPitchBtn.innerHTML = originalText;
                    copyPitchBtn.style.background = "";
                }, 2000);
            }).catch(err => {
                console.error("Failed to copy pitch text: ", err);
            });
        });
    }
});
