<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SentinelShield — Automated Dark-Pattern & Scam Contract Auditor</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Tailwind Configuration -->
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#ecfdf5',
              100: '#d1fae5',
              400: '#34d399',
              500: '#10b981',
              600: '#059669',
              900: '#064e3b',
            },
            cyber: {
              dark: '#0a0f1d',
              card: 'rgba(15, 23, 42, 0.75)',
              border: 'rgba(51, 65, 85, 0.6)',
              glow: '#00f2fe',
              accent: '#38bdf8'
            }
          },
          fontFamily: {
            sans: ['Inter', 'system-ui', 'sans-serif'],
            mono: ['Fira Code', 'JetBrains Mono', 'monospace']
          },
          animation: {
            'pulse-glow': 'pulseGlow 2.5s infinite alternate',
            'scan-line': 'scanLine 3s linear infinite',
            'radar-spin': 'radarSpin 4s linear infinite',
          },
          keyframes: {
            pulseGlow: {
              '0%': { boxShadow: '0 0 10px rgba(16, 185, 129, 0.2), inset 0 0 10px rgba(16, 185, 129, 0.1)' },
              '100%': { boxShadow: '0 0 25px rgba(16, 185, 129, 0.6), inset 0 0 15px rgba(16, 185, 129, 0.3)' }
            },
            scanLine: {
              '0%': { top: '0%' },
              '100%': { top: '100%' }
            },
            radarSpin: {
              '0%': { transform: 'rotate(0deg)' },
              '100%': { transform: 'rotate(360deg)' }
            }
          }
        }
      }
    }
  </script>

  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

  <style>
    body {
      background-color: #060913;
      color: #f1f5f9;
      font-family: 'Inter', sans-serif;
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(16, 185, 129, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
        linear-gradient(to right, rgba(15, 23, 42, 0.3) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(15, 23, 42, 0.3) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 30px 30px, 30px 30px;
    }

    .glass-panel {
      background: rgba(13, 20, 36, 0.75);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(51, 65, 85, 0.5);
    }

    .glass-panel-glow {
      background: rgba(13, 20, 36, 0.85);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(16, 185, 129, 0.4);
      box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #090d16;
    }
    ::-webkit-scrollbar-thumb {
      background: #1e293b;
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #10b981;
    }

    /* Score Gauge Progress */
    .gauge-circle {
      transition: stroke-dashoffset 1s ease-in-out;
    }

    .terminal-text {
      font-family: 'Fira Code', monospace;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-brand-500 selection:text-black">

  <!-- TOP HEADER -->
  <header class="sticky top-0 z-50 glass-panel border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        
        <!-- Logo & Branding -->
        <div class="flex items-center gap-3">
          <div class="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500 to-emerald-700 text-slate-950 font-bold shadow-lg shadow-brand-500/20">
            <i data-lucide="shield-alert" class="w-6 h-6 text-slate-950"></i>
            <span class="absolute -top-1 -right-1 flex h-3 w-3">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3 w-3 bg-brand-500"></span>
            </span>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xl font-extrabold tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-brand-400">
                SENTINEL<span class="text-brand-400">SHIELD</span>
              </span>
              <span class="text-[10px] px-2 py-0.5 rounded-full font-mono bg-brand-500/10 text-brand-400 border border-brand-500/30">v2.4-PROD</span>
            </div>
            <p class="text-[11px] text-slate-400 hidden sm:block">Automated Dark-Pattern & Scam Contract Auditor</p>
          </div>
        </div>

        <!-- Agent & Engine Status Badges -->
        <div class="hidden lg:flex items-center gap-3">
          <div class="flex items-center gap-2 text-xs font-mono px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-300">
            <i data-lucide="bot" class="w-4 h-4 text-cyan-400 animate-pulse"></i>
            <span>TinyFish Agent: <strong class="text-emerald-400">ACTIVE</strong></span>
          </div>
          <div class="flex items-center gap-2 text-xs font-mono px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-300">
            <i data-lucide="brain-circuit" class="w-4 h-4 text-brand-400"></i>
            <span>LLM Inspector: <strong class="text-brand-400">ONLINE</strong></span>
          </div>
        </div>

        <!-- Navigation Tabs -->
        <nav class="flex items-center gap-1 sm:gap-2">
          <button onclick="switchTab('scanner')" id="tab-btn-scanner" class="tab-btn px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-all duration-200 flex items-center gap-1.5 bg-brand-500/20 text-brand-400 border border-brand-500/40">
            <i data-lucide="radar" class="w-4 h-4"></i>
            <span>Audit Scanner</span>
          </button>
          <button onclick="switchTab('library')" id="tab-btn-library" class="tab-btn px-3 py-2 rounded-lg text-xs sm:text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800/60 transition-all duration-200 flex items-center gap-1.5">
            <i data-lucide="book-open" class="w-4 h-4"></i>
            <span>Dark Pattern DB</span>
          </button>
          <button onclick="switchTab('calculator')" id="tab-btn-calculator" class="tab-btn px-3 py-2 rounded-lg text-xs sm:text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800/60 transition-all duration-200 flex items-center gap-1.5">
            <i data-lucide="calculator" class="w-4 h-4"></i>
            <span>Risk Simulator</span>
          </button>
          <button onclick="switchTab('history')" id="tab-btn-history" class="tab-btn px-3 py-2 rounded-lg text-xs sm:text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800/60 transition-all duration-200 flex items-center gap-1.5">
            <i data-lucide="history" class="w-4 h-4"></i>
            <span>Audit Logs</span>
          </button>
        </nav>
      </div>
    </div>
  </header>

  <!-- MAIN WRAPPER -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-grow w-full">

    <!-- TAB 1: AUDIT SCANNER (MAIN WORKFLOW) -->
    <div id="tab-scanner" class="tab-content space-y-6">

      <!-- HERO INPUT BANNER -->
      <div class="glass-panel rounded-2xl p-6 sm:p-8 relative overflow-hidden">
        <div class="absolute -right-16 -top-16 w-64 h-64 bg-brand-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="absolute -left-16 -bottom-16 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div class="relative z-10 max-w-3xl">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700/80 text-xs text-brand-400 mb-3 font-mono">
            <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
            <span>Autonomous Web Crawling & Legal Parsing Engine</span>
          </div>
          <h1 class="text-2xl sm:text-4xl font-extrabold tracking-tight text-white mb-3">
            Expose Hidden Traps, Auto-Debits & Shady Terms in Seconds
          </h1>
          <p class="text-slate-300 text-sm sm:text-base mb-6 leading-relaxed">
            Enter any suspicious URL or paste a contract agreement. <strong class="text-brand-400">TinyFish Browser Agent</strong> will autonomously navigate popups, click hidden terms links, bypass consent traps, and highlight scam risks.
          </p>

          <!-- Input Controls -->
          <div class="space-y-4">
            <div class="relative flex flex-col sm:flex-row items-stretch gap-2">
              <div class="relative flex-grow">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                  <i data-lucide="globe" class="w-5 h-5"></i>
                </div>
                <input 
                  type="text" 
                  id="target-url-input" 
                  placeholder="https://suspicious-loan-app.com/checkout or paste terms..."
                  value="https://instant-cashloan-india.app/apply-now"
                  class="w-full pl-11 pr-4 py-3.5 bg-slate-900/90 border border-slate-700/80 rounded-xl text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-all shadow-inner font-mono"
                >
              </div>
              <button 
                onclick="runAuditScan()" 
                id="start-audit-btn"
                class="px-6 py-3.5 bg-gradient-to-r from-brand-500 to-emerald-600 hover:from-brand-400 hover:to-emerald-500 text-slate-950 font-bold text-sm rounded-xl transition-all duration-200 flex items-center justify-center gap-2 shadow-lg shadow-brand-500/25 active:scale-95 whitespace-nowrap"
              >
                <i data-lucide="shield-search" class="w-5 h-5"></i>
                <span>Trigger Agent Audit</span>
              </button>
            </div>

            <!-- Quick Presets -->
            <div class="flex flex-wrap items-center gap-2 pt-2">
              <span class="text-xs text-slate-400 font-medium mr-1">Quick Presets:</span>
              
              <button onclick="loadPreset('loan')" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700/60 text-slate-300 hover:text-white transition-all flex items-center gap-1.5">
                <i data-lucide="landmark" class="w-3.5 h-3.5 text-amber-400"></i>
                <span>Shady Loan App</span>
              </button>
              
              <button onclick="loadPreset('saas')" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700/60 text-slate-300 hover:text-white transition-all flex items-center gap-1.5">
                <i data-lucide="refresh-cw" class="w-3.5 h-3.5 text-cyan-400"></i>
                <span>Sneaky SaaS Sub</span>
              </button>

              <button onclick="loadPreset('ecom')" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700/60 text-slate-300 hover:text-white transition-all flex items-center gap-1.5">
                <i data-lucide="shopping-cart" class="w-3.5 h-3.5 text-rose-400"></i>
                <span>E-Commerce Flash Trap</span>
              </button>

              <button onclick="loadPreset('trial')" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700/60 text-slate-300 hover:text-white transition-all flex items-center gap-1.5">
                <i data-lucide="gift" class="w-3.5 h-3.5 text-purple-400"></i>
                <span>Free Trial Trap</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- TINYFISH AGENT INTERACTIVE WORKFLOW DISPLAY -->
      <div id="agent-execution-box" class="glass-panel rounded-2xl p-6 hidden transition-all duration-300">
        <div class="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
          <div class="flex items-center gap-3">
            <div class="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
              <i data-lucide="bot" class="w-5 h-5 animate-spin"></i>
            </div>
            <div>
              <h3 class="text-sm font-semibold text-white">TinyFish Autonomous Agent Execution</h3>
              <p class="text-xs text-slate-400" id="agent-current-status">Initializing headless browser environment...</p>
            </div>
          </div>
          <div class="text-xs font-mono px-3 py-1 rounded bg-slate-900 border border-slate-800 text-cyan-400 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
            <span id="agent-progress-pct">0%</span>
          </div>
        </div>

        <!-- Grid layout: Terminal Logs + Visual DOM Crawler View -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
          
          <!-- Terminal Logs -->
          <div class="lg:col-span-7 bg-slate-950 rounded-xl p-4 border border-slate-800 terminal-text text-xs text-slate-300 h-64 overflow-y-auto space-y-2 shadow-inner" id="agent-logs-container">
            <!-- Dynamic logs inserted via JS -->
          </div>

          <!-- Browser Agent Viewfinder -->
          <div class="lg:col-span-5 bg-slate-900/90 rounded-xl border border-slate-800 p-4 flex flex-col justify-between relative overflow-hidden">
            <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
              <span class="text-[11px] font-mono text-slate-400 flex items-center gap-1.5">
                <i data-lucide="chrome" class="w-3.5 h-3.5 text-slate-500"></i>
                Headless Viewfinder
              </span>
              <span class="text-[10px] font-mono text-brand-400 bg-brand-500/10 px-2 py-0.5 rounded" id="dom-target-badge">
                DOM Inspector
              </span>
            </div>

            <!-- Simulated Browser Canvas Frame -->
            <div class="my-3 flex-grow bg-slate-950 rounded-lg border border-slate-800/80 p-3 relative flex flex-col justify-center items-center text-center overflow-hidden">
              <div id="viewfinder-pulse-overlay" class="absolute inset-0 bg-brand-500/5 opacity-0 transition-opacity"></div>
              
              <div id="viewfinder-content" class="space-y-3 z-10 w-full px-4">
                <i data-lucide="file-search" class="w-8 h-8 mx-auto text-slate-600"></i>
                <p class="text-xs text-slate-400">Agent navigating page elements...</p>
              </div>
            </div>

            <div class="flex justify-between items-center text-[10px] text-slate-500 font-mono pt-1">
              <span>View: 1920x1080 (Chromium)</span>
              <span>Bypassing Captcha...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- RESULTS DASHBOARD (RENDERED ON COMPLETE) -->
      <div id="audit-results-dashboard" class="space-y-6 hidden">

        <!-- RISK SCORE & OVERVIEW TOP CARD -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          <!-- Gauge Card -->
          <div class="lg:col-span-5 glass-panel-glow rounded-2xl p-6 flex flex-col justify-between items-center text-center relative">
            <div class="w-full flex justify-between items-center mb-2">
              <span class="text-xs font-mono text-slate-400 flex items-center gap-1.5">
                <i data-lucide="shield-check" class="w-4 h-4 text-brand-400"></i>
                AI AUDIT VERDICT
              </span>
              <span id="risk-severity-badge" class="px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-rose-500/20 text-rose-400 border border-rose-500/40">
                CRITICAL RISK
              </span>
            </div>

            <!-- Circular Gauge -->
            <div class="relative my-4 flex items-center justify-center">
              <svg class="w-48 h-48 transform -rotate-90">
                <circle cx="96" cy="96" r="76" stroke="currentColor" stroke-width="12" class="text-slate-800" fill="transparent" />
                <circle id="risk-gauge-circle" cx="96" cy="96" r="76" stroke="currentColor" stroke-width="12" class="text-rose-500 gauge-circle" fill="transparent" stroke-dasharray="477" stroke-dashoffset="477" stroke-linecap="round" />
              </svg>
              <div class="absolute flex flex-col items-center justify-center">
                <span id="risk-score-value" class="text-4xl sm:text-5xl font-black text-white font-mono">0%</span>
                <span class="text-xs text-slate-400 font-mono mt-1">Scam / Trap Score</span>
              </div>
            </div>

            <!-- Target Meta Info -->
            <div class="w-full bg-slate-900/80 rounded-xl p-3 border border-slate-800 text-left text-xs font-mono space-y-1">
              <div class="flex justify-between">
                <span class="text-slate-500">Target Site:</span>
                <span id="meta-target-site" class="text-slate-200 truncate max-w-[200px]">instant-cashloan.app</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-500">Legal Pages Scanned:</span>
                <span class="text-emerald-400">4 Pages (Checkout, T&C, Terms)</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-500">Hidden Traps Found:</span>
                <span id="meta-traps-count" class="text-rose-400 font-bold">5 Violations</span>
              </div>
            </div>
          </div>

          <!-- Summary & Quick Stats -->
          <div class="lg:col-span-7 glass-panel rounded-2xl p-6 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-3">
                <h2 class="text-lg font-bold text-white flex items-center gap-2">
                  <i data-lucide="file-warning" class="w-5 h-5 text-amber-400"></i>
                  <span>Executive Legal Audit Summary</span>
                </h2>
                <button onclick="exportAuditPDF()" class="text-xs px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 flex items-center gap-1.5 transition">
                  <i data-lucide="download" class="w-3.5 h-3.5"></i>
                  <span>Export Report PDF</span>
                </button>
              </div>

              <p id="audit-summary-text" class="text-slate-300 text-sm leading-relaxed mb-4">
                Analysis complete. SentinelShield detected severe dark patterns designed to lock users into non-consensual automated debit mandates, hidden recurring membership fees, and mandatory contact list scraping disguised as identity verification.
              </p>

              <h4 class="text-xs font-mono text-slate-400 uppercase tracking-wider mb-2">Detected Dark Pattern Categories</h4>
              <div id="detected-pattern-tags" class="flex flex-wrap gap-2 mb-4">
                <!-- Dynamic Pattern Badges -->
              </div>
            </div>

            <!-- Quick Action Shield Bar -->
            <div class="bg-brand-500/10 border border-brand-500/30 rounded-xl p-4 flex flex-col sm:flex-row items-center justify-between gap-3">
              <div class="flex items-center gap-3">
                <div class="p-2 rounded-lg bg-brand-500/20 text-brand-400">
                  <i data-lucide="shield-alert" class="w-5 h-5"></i>
                </div>
                <div>
                  <h4 class="text-xs font-bold text-white">Recommended Action Status</h4>
                  <p class="text-[11px] text-slate-300">Do not enter banking or personal credentials on this domain.</p>
                </div>
              </div>
              <button onclick="scrollToDefenseSection()" class="w-full sm:w-auto px-4 py-2 bg-brand-500 text-slate-950 font-bold text-xs rounded-lg hover:bg-brand-400 transition flex items-center justify-center gap-1.5 whitespace-nowrap">
                <span>View Defense Checklist</span>
                <i data-lucide="arrow-down" class="w-3.5 h-3.5"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- DETAILED RED FLAGS BREAKDOWN -->
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-bold text-white flex items-center gap-2">
              <i data-lucide="alert-triangle" class="w-5 h-5 text-rose-400"></i>
              <span>Highlighted Predatory Clauses & Hidden Rules</span>
            </h3>
            <span class="text-xs text-slate-400 font-mono">LLM Extraction Precision: 99.2%</span>
          </div>

          <!-- Red Flag Cards Container -->
          <div id="red-flags-container" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Dynamically Populated by JS -->
          </div>
        </div>

        <!-- ACTIONABLE DEFENSE & OPT-OUT LETTER GENERATOR -->
        <div id="defense-section" class="glass-panel rounded-2xl p-6 space-y-6">
          <div class="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h3 class="text-lg font-bold text-white flex items-center gap-2">
                <i data-lucide="shield-check" class="w-5 h-5 text-emerald-400"></i>
                <span>Actionable Defense & One-Click Shielding</span>
              </h3>
              <p class="text-xs text-slate-400 mt-0.5">Steps to protect yourself + auto-generated cancellation/opt-out legal notice</p>
            </div>
            <span class="px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-mono">Consumer Rights Protected</span>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <!-- Checklist -->
            <div class="lg:col-span-5 space-y-3">
              <h4 class="text-xs font-mono uppercase text-slate-400 tracking-wider">Immediate Protection Steps</h4>
              
              <div class="p-3 bg-slate-900/80 rounded-xl border border-slate-800 flex items-start gap-3">
                <div class="p-1.5 rounded bg-amber-500/10 text-amber-400 mt-0.5">
                  <i data-lucide="credit-card" class="w-4 h-4"></i>
                </div>
                <div>
                  <h5 class="text-xs font-semibold text-white">Block UPI Auto-Mandate</h5>
                  <p class="text-[11px] text-slate-400">Revoke any standing auto-debit approval inside Google Pay, PhonePe, or Paytm settings immediately.</p>
                </div>
              </div>

              <div class="p-3 bg-slate-900/80 rounded-xl border border-slate-800 flex items-start gap-3">
                <div class="p-1.5 rounded bg-cyan-500/10 text-cyan-400 mt-0.5">
                  <i data-lucide="lock" class="w-4 h-4"></i>
                </div>
                <div>
                  <h5 class="text-xs font-semibold text-white">Use Virtual Disposable Card</h5>
                  <p class="text-[11px] text-slate-400">If forced to pay trial fees, use a single-use virtual card with a $1 limit to prevent drip pricing.</p>
                </div>
              </div>

              <div class="p-3 bg-slate-900/80 rounded-xl border border-slate-800 flex items-start gap-3">
                <div class="p-1.5 rounded bg-rose-500/10 text-rose-400 mt-0.5">
                  <i data-lucide="users" class="w-4 h-4"></i>
                </div>
                <div>
                  <h5 class="text-xs font-semibold text-white">Revoke Mobile Contacts Permission</h5>
                  <p class="text-[11px] text-slate-400">Go to OS App Settings -> Privacy -> Permissions -> Revoke Contact Sync to prevent contact harassment.</p>
                </div>
              </div>
            </div>

            <!-- One-Click Legal Opt-Out / Revocation Generator -->
            <div class="lg:col-span-7 bg-slate-900/90 rounded-xl p-4 border border-slate-800 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <h4 class="text-xs font-mono uppercase text-brand-400 tracking-wider flex items-center gap-1.5">
                    <i data-lucide="mail-warning" class="w-4 h-4"></i>
                    <span>Automated Opt-Out & Revocation Email Generator</span>
                  </h4>
                  <button onclick="copyOptOutEmail()" class="text-xs px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center gap-1">
                    <i data-lucide="copy" class="w-3 h-3"></i>
                    <span>Copy Text</span>
                  </button>
                </div>

                <div class="bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs font-mono text-slate-300 h-44 overflow-y-auto" id="opt-out-letter-box">
                  <!-- Dynamic legal letter -->
                </div>
              </div>

              <div class="pt-3 flex justify-between items-center text-[11px] text-slate-500">
                <span>Based on Consumer Protection Act & RBI Cyber Directives</span>
                <span class="text-emerald-400 font-mono flex items-center gap-1">
                  <i data-lucide="check-circle2" class="w-3 h-3"></i> Ready to send
                </span>
              </div>
            </div>

          </div>
        </div>

      </div>

    </div>

    <!-- TAB 2: DARK PATTERN LIBRARY & KNOWLEDGE BASE -->
    <div id="tab-library" class="tab-content space-y-6 hidden">
      <div class="glass-panel rounded-2xl p-6">
        <div class="max-w-3xl mb-6">
          <h2 class="text-xl sm:text-2xl font-bold text-white mb-2 flex items-center gap-2">
            <i data-lucide="book-open" class="w-6 h-6 text-brand-400"></i>
            <span>Dark Pattern Database & Legal Reference</span>
          </h2>
          <p class="text-slate-300 text-sm">
            Top deceptive design patterns and predatory clauses identified across e-commerce, instant loan apps, and subscription platforms in modern digital markets.
          </p>
        </div>

        <!-- Pattern Filter Buttons -->
        <div class="flex flex-wrap gap-2 mb-6">
          <button onclick="filterPatternLib('all')" class="pattern-filter-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-brand-500/20 text-brand-400 border border-brand-500/30">All Patterns</button>
          <button onclick="filterPatternLib('loan')" class="pattern-filter-btn px-3 py-1.5 rounded-lg text-xs font-medium text-slate-400 hover:bg-slate-800 border border-slate-800">Financial / Loan Traps</button>
          <button onclick="filterPatternLib('saas')" class="pattern-filter-btn px-3 py-1.5 rounded-lg text-xs font-medium text-slate-400 hover:bg-slate-800 border border-slate-800">Subscription & Auto-Debit</button>
          <button onclick="filterPatternLib('ecom')" class="pattern-filter-btn px-3 py-1.5 rounded-lg text-xs font-medium text-slate-400 hover:bg-slate-800 border border-slate-800">E-Commerce & Urgency</button>
        </div>

        <!-- Patterns Cards Grid -->
        <div id="pattern-db-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- Populated by JS -->
        </div>
      </div>
    </div>

    <!-- TAB 3: RISK SCORE CALCULATOR / QUIZ -->
    <div id="tab-calculator" class="tab-content space-y-6 hidden">
      <div class="glass-panel rounded-2xl p-6">
        <div class="max-w-3xl mb-6">
          <h2 class="text-xl sm:text-2xl font-bold text-white mb-2 flex items-center gap-2">
            <i data-lucide="calculator" class="w-6 h-6 text-cyan-400"></i>
            <span>Interactive Risk Score Simulator</span>
          </h2>
          <p class="text-slate-300 text-sm">
            Evaluate a contract or service manually by checking the presence of specific clauses and UI conditions.
          </p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <!-- Quiz Options -->
          <div class="lg:col-span-7 space-y-4">
            <div class="p-4 bg-slate-900/80 rounded-xl border border-slate-800 space-y-3">
              <label class="flex items-start gap-3 cursor-pointer">
                <input type="checkbox" onchange="calculateManualRisk()" class="sim-check mt-1 rounded bg-slate-950 border-slate-700 text-brand-500 focus:ring-brand-500 w-4 h-4" data-weight="25">
                <div>
                  <span class="text-sm font-semibold text-white block">Mandatory Auto-Debit or UPI e-Mandate required before trial</span>
                  <span class="text-xs text-slate-400 block">Requires payment details and recurring authorization up front.</span>
                </div>
              </label>
            </div>

            <div class="p-4 bg-slate-900/80 rounded-xl border border-slate-800 space-y-3">
              <label class="flex items-start gap-3 cursor-pointer">
                <input type="checkbox" onchange="calculateManualRisk()" class="sim-check mt-1 rounded bg-slate-950 border-slate-700 text-brand-500 focus:ring-brand-500 w-4 h-4" data-weight="20">
                <div>
                  <span class="text-sm font-semibold text-white block">Pre-checked boxes for insurance, add-ons, or newsletter consent</span>
                  <span class="text-xs text-slate-400 block">Default options that add extra cost or opt user into data sharing.</span>
                </div>
              </label>
            </div>

            <div class="p-4 bg-slate-900/80 rounded-xl border border-slate-800 space-y-3">
              <label class="flex items-start gap-3 cursor-pointer">
                <input type="checkbox" onchange="calculateManualRisk()" class="sim-check mt-1 rounded bg-slate-950 border-slate-700 text-brand-500 focus:ring-brand-500 w-4 h-4" data-weight="20">
                <div>
                  <span class="text-sm font-semibold text-white block">No online cancellation option (Must call or email support)</span>
                  <span class="text-xs text-slate-400 block">Roach motel design: Easy to enter, friction-heavy to exit.</span>
                </div>
              </label>
            </div>

            <div class="p-4 bg-slate-900/80 rounded-xl border border-slate-800 space-y-3">
              <label class="flex items-start gap-3 cursor-pointer">
                <input type="checkbox" onchange="calculateManualRisk()" class="sim-check mt-1 rounded bg-slate-950 border-slate-700 text-brand-500 focus:ring-brand-500 w-4 h-4" data-weight="20">
                <div>
                  <span class="text-sm font-semibold text-white block">Access to phone contacts or photo gallery requested for loan/service</span>
                  <span class="text-xs text-slate-400 block">Aggressive data harvesting often used for blackmailing in loan scams.</span>
                </div>
              </label>
            </div>

            <div class="p-4 bg-slate-900/80 rounded-xl border border-slate-800 space-y-3">
              <label class="flex items-start gap-3 cursor-pointer">
                <input type="checkbox" onchange="calculateManualRisk()" class="sim-check mt-1 rounded bg-slate-950 border-slate-700 text-brand-500 focus:ring-brand-500 w-4 h-4" data-weight="15">
                <div>
                  <span class="text-sm font-semibold text-white block">Fake urgency timers or fake stock level alerts</span>
                  <span class="text-xs text-slate-400 block">Countdowns that reset on refresh to manipulate impulse buying.</span>
                </div>
              </label>
            </div>
          </div>

          <!-- Live Score Result Box -->
          <div class="lg:col-span-5 glass-panel-glow rounded-xl p-6 flex flex-col justify-between items-center text-center">
            <h3 class="text-xs font-mono uppercase text-slate-400">Calculated Scam Probability</h3>
            
            <div class="my-6">
              <span id="sim-score-text" class="text-5xl font-black font-mono text-emerald-400">0%</span>
              <p id="sim-verdict-text" class="text-xs text-slate-300 font-medium mt-2">Low Risk / Standard Terms</p>
            </div>

            <div class="w-full bg-slate-950 p-4 rounded-xl border border-slate-800 text-left text-xs font-mono space-y-2">
              <div class="text-slate-400">Recommendation:</div>
              <p id="sim-recommendation" class="text-slate-200">Safe to proceed with normal caution. Ensure you review the full privacy policy.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: AUDIT HISTORY & REPORT LOGS -->
    <div id="tab-history" class="tab-content space-y-6 hidden">
      <div class="glass-panel rounded-2xl p-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <h2 class="text-xl sm:text-2xl font-bold text-white flex items-center gap-2">
              <i data-lucide="history" class="w-6 h-6 text-brand-400"></i>
              <span>Recent Scan Records & Legal Audit Logs</span>
            </h2>
            <p class="text-slate-300 text-xs sm:text-sm">Filter and review past domain scans stored in SentinelShield registry.</p>
          </div>

          <div class="flex items-center gap-2">
            <input type="text" id="history-search-input" onkeyup="filterHistoryTable()" placeholder="Search domain..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-brand-500 font-mono">
          </div>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-slate-900/90 text-slate-400 font-mono uppercase text-[10px] border-b border-slate-800">
              <tr>
                <th class="p-3">Domain / App Title</th>
                <th class="p-3">Category</th>
                <th class="p-3">Risk Score</th>
                <th class="p-3">Primary Dark Pattern</th>
                <th class="p-3">Timestamp</th>
                <th class="p-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody id="history-table-body" class="divide-y divide-slate-800/60 font-mono text-slate-300">
              <!-- Dynamically populated by JS -->
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </main>

  <!-- MODAL FOR DETAILED REPORT VIEW -->
  <div id="report-modal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm hidden">
    <div class="glass-panel-glow rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 space-y-4">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <i data-lucide="file-text" class="w-5 h-5 text-brand-400"></i>
          <h3 class="text-base font-bold text-white">Full Legal Audit Report export</h3>
        </div>
        <button onclick="closeModal()" class="text-slate-400 hover:text-white p-1">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div id="modal-report-content" class="text-xs font-mono bg-slate-950 p-4 rounded-xl border border-slate-800 text-slate-300 whitespace-pre-wrap leading-relaxed">
        <!-- Dynamic content -->
      </div>

      <div class="flex justify-end gap-2 pt-2">
        <button onclick="closeModal()" class="px-4 py-2 bg-slate-800 text-slate-300 rounded-lg text-xs hover:bg-slate-700">Close</button>
        <button onclick="window.print()" class="px-4 py-2 bg-brand-500 text-slate-950 font-bold rounded-lg text-xs hover:bg-brand-400 flex items-center gap-1.5">
          <i data-lucide="printer" class="w-4 h-4"></i>
          <span>Print / Save PDF</span>
        </button>
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <footer class="border-t border-slate-800/80 bg-slate-950/80 py-4 text-center text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2 font-mono">
      <span>© 2026 SentinelShield AI • Powered by TinyFish Headless Engine & Legal LLM</span>
      <span class="flex items-center gap-1 text-slate-400">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        Consumer Protection Directives Active
      </span>
    </div>
  </footer>

  <!-- JAVASCRIPT LOGIC -->
  <script>
    // PRESET CONTRACT SAMPLES
    const SAMPLE_PRESETS = {
      loan: {
        url: "https://instant-cashloan-india.app/apply-now",
        category: "Instant Loan App",
        score: 92,
        severity: "CRITICAL RISK",
        summary: "High risk identified! The terms contain predatory daily interest escalation clauses, auto-debit mandates without prior SMS warnings, and mandatory consent to contact phonebook numbers in case of payment delay.",
        patterns: ["Unauthorised Auto-Debit", "Aggressive Contact Scraping", "Drip Processing Fees", "Hidden Daily Interest Penalty"],
        redFlags: [
          {
            title: "Mandatory Phonebook & Contact Access Consent",
            category: "Data Scraping",
            risk: "CRITICAL",
            quote: "\"By clicking Accept, the Borrower grants unrestricted permission to access, upload, and retain the complete contact list from the mobile device to contact relatives and acquaintances upon default.\"",
            meaning: "They will message and harass your family and friends if payment is delayed by even 24 hours.",
            icon: "users"
          },
          {
            title: "Automated UPI e-Mandate Penalty Clause",
            category: "Financial Trap",
            risk: "HIGH",
            quote: "\"Borrower agrees to auto-debit deduction on the 1st of each month. Failed debits incur a ₹750 bounce charge + daily 2.5% compounding fee automatically billed.\"",
            meaning: "They will repeatedly charge your bank account, accumulating heavy bounce fees even if your account balance is zero.",
            icon: "credit-card"
          },
          {
            title: "Hidden 18% Upfront Processing Deduction",
            category: "Drip Pricing",
            risk: "HIGH",
            quote: "\"Sanctioned amount will be disbursed after deducting a non-refundable Platform Technology & Advisory Fee of 18%.\"",
            meaning: "You only get 82% of the loan amount, but you have to pay interest on 100% of the loan amount.",
            icon: "coins"
          }
        ],
        optOutEmail: `TO: grievance@instant-cashloan-india.app\nSUBJECT: Immediate Revocation of Contact Access & e-Mandate Cancel Notice - Ref #[REDACTED]\n\nDear Nodal Officer,\n\nI hereby formally revoke consent for your application to access, store, or contact my mobile contact book per RBI Digital Lending Guidelines 2022.\n\nFurthermore, I cancel all standing e-Mandate auto-debit authorizations linked to my UPI/Account with immediate effect.\n\nAny attempt to harass third parties will be reported directly to the Cyber Crime Cell and Reserve Bank of India.\n\nRegards,\n[Your Name]`
      },
      saas: {
        url: "https://cloud-design-studio.io/subscribe-pro",
        category: "Subscription SaaS",
        score: 78,
        severity: "HIGH RISK",
        summary: "Roach Motel pattern detected! Free 7-day trial automatically converts into a mandatory non-refundable $299 annual commitment with no digital cancel button on the portal.",
        patterns: ["Forced Annual Continuity", "Hard-to-Cancel (Roach Motel)", "Pre-checked Auto-Renew"],
        redFlags: [
          {
            title: "Invisible Annual Conversion Trap",
            category: "Auto-Debit",
            risk: "HIGH",
            quote: "\"After the 7-day trial period, subscription automatically rolls over into a 12-month non-cancelable annual plan billed upfront at $299.\"",
            meaning: "Instead of monthly charges, you will be hit with a surprise $299 full-year charge immediately when the trial ends.",
            icon: "calendar-x"
          },
          {
            title: "Cancellation Friction (No Online Button)",
            category: "Roach Motel",
            risk: "CRITICAL",
            quote: "\"Cancellations must be requested via certified postal letter or telephone call to our international support desk during operating hours (Mon-Fri 9AM-11AM EST).\"",
            meaning: "They make it almost impossible to cancel online, forcing you to stay subscribed.",
            icon: "phone-off"
          }
        ],
        optOutEmail: `TO: billing@cloud-design-studio.io\nSUBJECT: Notice of Trial Cancellation & Prohibition of Auto-Renewal\n\nTo Customer Billing Support,\n\nPlease accept this email as formal written notice to cancel my trial subscription for Account: [Your Email] effective immediately.\n\nUnder consumer digital privacy rules, I explicitly prohibit any automated debit charges to my credit card upon expiration of the trial period.\n\nConfirmation of cancellation is requested within 24 hours.\n\nRegards,\n[Your Name]`
      },
      ecom: {
        url: "https://flash-deal-electronics.shop/checkout",
        category: "E-Commerce Flash Sale",
        score: 64,
        severity: "MODERATE RISK",
        summary: "E-commerce trickery found! Pre-checked insurance and VIP delivery add-ons added to total cart cost, combined with a fake ticking countdown timer designed to push impulse payment.",
        patterns: ["Sneaky Basket Add-ons", "Fake Scarcity Timer", "Non-refundable Store Credit"],
        redFlags: [
          {
            title: "Sneaky Pre-selected Basket Charges",
            category: "Hidden Fees",
            risk: "MEDIUM",
            quote: "\"VIP Express Warranty ($14.99) and Shipping Protection ($4.99) are pre-selected for your order security.\"",
            meaning: "Extra items were silently added to your total bill without your explicit click consent.",
            icon: "shopping-bag"
          },
          {
            title: "Refund Issued Only As Non-Transferable Tokens",
            category: "Restrictive Policy",
            risk: "HIGH",
            quote: "\"Cash refunds are strictly prohibited. Returned items will receive store credits expiring in 30 days.\"",
            meaning: "You will never get your original money back, even if they send damaged or wrong goods.",
            icon: "rotate-ccw"
          }
        ],
        optOutEmail: `TO: support@flash-deal-electronics.shop\nSUBJECT: Order Amendment Notice - Removal of Unsolicited Add-ons - Order #[REDACTED]\n\nDear Support,\n\nI am requesting the immediate removal of pre-selected VIP Warranty and Shipping Protection fees from my pending order.\n\nUnder E-Commerce Consumer Directives, pre-checked boxes for paid add-ons are illegal.\n\nRegards,\n[Your Name]`
      },
      trial: {
        url: "https://fit-life-nutra.co/free-bottle-trial",
        category: "Free Trial Trap",
        score: 85,
        severity: "HIGH RISK",
        summary: "Free Trial Scam! User pays $4.95 for shipping, but hides an automatic monthly recurring charge of $89.95 every 30 days hidden in sub-clause 14.B.",
        patterns: ["Drip Pricing", "Hidden Recurring Mandate", "Obscured Terms Text"],
        redFlags: [
          {
            title: "Hidden $89.95 Monthly Auto-Ship Clause",
            category: "Hidden Continuity",
            risk: "CRITICAL",
            quote: "\"By paying $4.95 shipping, you enroll in our Monthly Vitality Club billed automatically at $89.95 every 30 days until canceled.\"",
            meaning: "The 'free' trial is a trick to get your credit card details for monthly automatic billing.",
            icon: "refresh-cw"
          }
        ],
        optOutEmail: `TO: support@fit-life-nutra.co\nSUBJECT: Immediate Cancellation of Club Membership & Recurring Mandate\n\nTo Customer Support,\n\nI am writing to cancel my enrollment in the Monthly Vitality Club associated with my recent trial shipping payment.\n\nDo not bill my card for recurring charges. Revoke all payment authorizations immediately.\n\nRegards,\n[Your Name]`
      }
    };

    // AUDIT HISTORY RECORD DATA
    let auditHistory = [
      { domain: "instant-cashloan-india.app", category: "Loan App", score: 92, pattern: "Auto-Debit & Contact Scraping", date: "2026-10-16 20:14" },
      { domain: "cloud-design-studio.io", category: "SaaS Sub", score: 78, pattern: "Roach Motel Cancellation", date: "2026-10-15 14:22" },
      { domain: "quick-rupee-loan.net", category: "Loan App", score: 96, pattern: "Harassment & 25% Daily Penalty", date: "2026-10-14 09:10" },
      { domain: "flash-deal-electronics.shop", category: "E-Commerce", score: 64, pattern: "Sneaky Basket Add-ons", date: "2026-10-12 18:45" },
      { domain: "stream-hub-premium.xyz", category: "Subscription", score: 81, pattern: "Hidden Auto-renew rollover", date: "2026-10-10 11:30" }
    ];

    // DARK PATTERN DATABASE ITEMS
    const PATTERN_DATABASE = [
      {
        title: "Roach Motel (Hard to Cancel)",
        category: "saas",
        severity: "CRITICAL",
        desc: "Making it extremely easy to subscribe (1-click) but intentionally convoluted to cancel (requires phone call or physical letter).",
        law: "Violates FTC Negative Option Rule & Consumer Protection Directives."
      },
      {
        title: "Forced UPI / Auto-Debit Mandate",
        category: "loan",
        severity: "CRITICAL",
        desc: "Forcing users to sign continuous auto-debit permissions under the guise of identity verification before viewing loan terms.",
        law: "Violates RBI Digital Lending Directives."
      },
      {
        title: "Contact Scraping & Harassment",
        category: "loan",
        severity: "CRITICAL",
        desc: "Extracting complete mobile phonebooks to harass contacts and relatives if payment is delayed.",
        law: "Violates Data Protection Act & Cyber Security Regulations."
      },
      {
        title: "Sneaky Basket / Drip Pricing",
        category: "ecom",
        severity: "HIGH",
        desc: "Adding hidden fees, express shipping, or warranty add-ons via pre-checked tickboxes during checkout.",
        law: "Banned under E-Commerce Guidelines."
      },
      {
        title: "Fake Urgency & False Scarcity",
        category: "ecom",
        severity: "MEDIUM",
        desc: "Countdowns and 'Only 2 items left' warnings that reset automatically upon page refresh to trigger panic buying.",
        law: "Misleading Commercial Practices Act."
      },
      {
        title: "Pre-Checked Consent Traps",
        category: "saas",
        severity: "HIGH",
        desc: "Defaulting checkboxes for marketing data sharing, cross-site tracking, or recurring renewals to 'ON'.",
        law: "Explicit Consent Requirement Violation."
      }
    ];

    let currentActiveAuditData = null;

    // TAB NAVIGATION
    function switchTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('bg-brand-500/20', 'text-brand-400', 'border', 'border-brand-500/40');
        btn.classList.add('text-slate-400');
      });

      document.getElementById(`tab-${tabId}`).classList.remove('hidden');
      const activeBtn = document.getElementById(`tab-btn-${tabId}`);
      if(activeBtn) {
        activeBtn.classList.remove('text-slate-400');
        activeBtn.classList.add('bg-brand-500/20', 'text-brand-400', 'border', 'border-brand-500/40');
      }

      if (tabId === 'library') renderPatternDatabase('all');
      if (tabId === 'history') renderHistoryTable();
    }

    // LOAD PRESET SAMPLES
    function loadPreset(presetKey) {
      const preset = SAMPLE_PRESETS[presetKey];
      if (!preset) return;
      document.getElementById('target-url-input').value = preset.url;
      runAuditScan(presetKey);
    }

    // RUN AGENT AUDIT SCAN SIMULATION
    function runAuditScan(presetKey = 'loan') {
      const urlInput = document.getElementById('target-url-input').value;
      const agentBox = document.getElementById('agent-execution-box');
      const resultsDashboard = document.getElementById('audit-results-dashboard');
      const logsContainer = document.getElementById('agent-logs-container');
      const progressText = document.getElementById('agent-progress-pct');
      const currentStatusText = document.getElementById('agent-current-status');
      const viewfinderContent = document.getElementById('viewfinder-content');

      const presetData = SAMPLE_PRESETS[presetKey] || SAMPLE_PRESETS['loan'];
      currentActiveAuditData = presetData;

      // Reset and Show Exec Box
      resultsDashboard.classList.add('hidden');
      agentBox.classList.remove('hidden');
      logsContainer.innerHTML = '';
      
      const agentSteps = [
        { pct: '15%', text: `[00:01] Launching Chromium Headless Instance... Connecting to ${urlInput}`, dom: "DOM Render Mode", icon: "globe" },
        { pct: '35%', text: "[00:02] Injecting TinyFish Agent DOM parser... Looking for 'Terms', 'Privacy', and Checkout popups.", dom: "Bypassing Consent Banners", icon: "mouse-pointer" },
        { pct: '55%', text: "[00:04] Clicking hidden modal buttons: 'View Full Contract Terms' & 'Fee Structure'", dom: "Expanding Hidden Clauses", icon: "layers" },
        { pct: '75%', text: "[00:06] Extracting raw text content (14,280 words). Passing to LLM Legal Inspector engine...", dom: "Parsing Legal Lexicon", icon: "brain-circuit" },
        { pct: '90%', text: "[00:08] AI Analysis complete! Flagging auto-debit mandates & predatory clauses...", dom: "Computing Scam Score", icon: "shield-alert" },
        { pct: '100%', text: "[00:09] Audit Report Generated Successfully!", dom: "Report Finalized", icon: "check-circle2" }
      ];

      let stepIdx = 0;
      const interval = setInterval(() => {
        if (stepIdx < agentSteps.length) {
          const step = agentSteps[stepIdx];
          progressText.innerText = step.pct;
          currentStatusText.innerText = step.text;
          
          const logEntry = document.createElement('div');
          logEntry.className = "flex items-center gap-2 text-emerald-400";
          logEntry.innerHTML = `<span class="text-slate-500">></span> <span>${step.text}</span>`;
          logsContainer.appendChild(logEntry);
          logsContainer.scrollTop = logsContainer.scrollHeight;

          viewfinderContent.innerHTML = `
            <i data-lucide="${step.icon}" class="w-8 h-8 mx-auto text-brand-400 animate-bounce"></i>
            <p class="text-xs text-slate-200 font-mono">${step.dom}</p>
            <p class="text-[10px] text-slate-500">${urlInput}</p>
          `;
          lucide.createIcons();

          stepIdx++;
        } else {
          clearInterval(interval);
          setTimeout(() => {
            renderAuditResults(presetData);
          }, 400);
        }
      }, 700);
    }

    // RENDER AUDIT RESULTS
    function renderAuditResults(data) {
      document.getElementById('agent-execution-box').classList.add('hidden');
      const resultsDashboard = document.getElementById('audit-results-dashboard');
      resultsDashboard.classList.remove('hidden');

      // Update Meta
      document.getElementById('meta-target-site').innerText = data.url.replace('https://', '').split('/')[0];
      document.getElementById('meta-traps-count').innerText = `${data.redFlags.length} Critical Traps`;
      document.getElementById('audit-summary-text').innerText = data.summary;

      // Update Gauge
      const scoreVal = document.getElementById('risk-score-value');
      const gaugeCircle = document.getElementById('risk-gauge-circle');
      const severityBadge = document.getElementById('risk-severity-badge');

      scoreVal.innerText = `${data.score}%`;
      
      // Circle Circumference = 2 * PI * 76 = 477.5
      const offset = 477.5 - (477.5 * data.score) / 100;
      gaugeCircle.style.strokeDashoffset = offset;

      if (data.score >= 75) {
        gaugeCircle.style.color = "#f43f5e"; // Rose
        severityBadge.className = "px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-rose-500/20 text-rose-400 border border-rose-500/40";
        severityBadge.innerText = "CRITICAL SCAM RISK";
      } else if (data.score >= 40) {
        gaugeCircle.style.color = "#fbbf24"; // Amber
        severityBadge.className = "px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-amber-500/20 text-amber-400 border border-amber-500/40";
        severityBadge.innerText = "MODERATE RISK";
      } else {
        gaugeCircle.style.color = "#10b981"; // Emerald
        severityBadge.className = "px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-400 border border-emerald-500/40";
        severityBadge.innerText = "LOW RISK";
      }

      // Render Pattern Tags
      const tagsContainer = document.getElementById('detected-pattern-tags');
      tagsContainer.innerHTML = data.patterns.map(p => `
        <span class="px-2.5 py-1 rounded-lg text-xs font-mono bg-slate-800 text-rose-300 border border-slate-700/80 flex items-center gap-1">
          <i data-lucide="tag" class="w-3 h-3 text-rose-400"></i> ${p}
        </span>
      `).join('');

      // Render Red Flags Cards
      const flagsContainer = document.getElementById('red-flags-container');
      flagsContainer.innerHTML = data.redFlags.map(flag => `
        <div class="glass-panel rounded-xl p-4 border-l-4 border-l-rose-500 space-y-3">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="p-1.5 rounded bg-rose-500/10 text-rose-400">
                <i data-lucide="${flag.icon}" class="w-4 h-4"></i>
              </div>
              <h4 class="text-sm font-bold text-white">${flag.title}</h4>
            </div>
            <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-rose-500/20 text-rose-400 border border-rose-500/30">
              ${flag.risk}
            </span>
          </div>

          <div class="bg-slate-950/80 p-3 rounded-lg border border-slate-800 font-mono text-xs text-slate-300 italic">
            ${flag.quote}
          </div>

          <div class="space-y-1">
            <span class="text-[10px] uppercase font-mono text-brand-400 font-semibold tracking-wider">Plain-English Translation:</span>
            <p class="text-xs text-slate-300 leading-relaxed">${flag.meaning}</p>
          </div>
        </div>
      `).join('');

      // Update Opt-Out Letter
      document.getElementById('opt-out-letter-box').innerText = data.optOutEmail;

      // Re-initialize icons
      lucide.createIcons();

      // Push to history table
      auditHistory.unshift({
        domain: data.url.replace('https://', '').split('/')[0],
        category: data.category,
        score: data.score,
        pattern: data.patterns[0],
        date: new Date().toISOString().replace('T', ' ').substring(0, 16)
      });
    }

    // COPY OPT OUT EMAIL
    function copyOptOutEmail() {
      const text = document.getElementById('opt-out-letter-box').innerText;
      navigator.clipboard.writeText(text);
      alert('Opt-out legal revocation notice copied to clipboard!');
    }

    // SCROLL TO DEFENSE
    function scrollToDefenseSection() {
      document.getElementById('defense-section').scrollIntoView({ behavior: 'smooth' });
    }

    // CALCULATE MANUAL RISK (TAB 3)
    function calculateManualRisk() {
      const checkboxes = document.querySelectorAll('.sim-check');
      let score = 0;
      checkboxes.forEach(cb => {
        if (cb.checked) {
          score += parseInt(cb.getAttribute('data-weight') || 0);
        }
      });

      const scoreText = document.getElementById('sim-score-text');
      const verdictText = document.getElementById('sim-verdict-text');
      const recommendationText = document.getElementById('sim-recommendation');

      scoreText.innerText = `${score}%`;

      if (score >= 70) {
        scoreText.className = "text-5xl font-black font-mono text-rose-500";
        verdictText.innerText = "CRITICAL RISK / High Scam Likelihood";
        recommendationText.innerText = "Avoid entering payment details. High probability of non-consensual recurring debits and data harvesting.";
      } else if (score >= 35) {
        scoreText.className = "text-5xl font-black font-mono text-amber-400";
        verdictText.innerText = "MODERATE RISK / Caution Advised";
        recommendationText.innerText = "Proceed with virtual card protection. Uncheck pre-selected add-ons before paying.";
      } else {
        scoreText.className = "text-5xl font-black font-mono text-emerald-400";
        verdictText.innerText = "LOW RISK / Standard Digital Contract";
        recommendationText.innerText = "Safe to proceed with normal caution. Ensure you review the full privacy policy.";
      }
    }

    // RENDER PATTERN DATABASE (TAB 2)
    function renderPatternDatabase(category) {
      const grid = document.getElementById('pattern-db-grid');
      const filtered = category === 'all' 
        ? PATTERN_DATABASE 
        : PATTERN_DATABASE.filter(item => item.category === category);

      grid.innerHTML = filtered.map(item => `
        <div class="bg-slate-900/90 rounded-xl p-4 border border-slate-800 space-y-3 hover:border-slate-700 transition">
          <div class="flex items-center justify-between">
            <h4 class="text-sm font-bold text-white">${item.title}</h4>
            <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30">
              ${item.severity}
            </span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">${item.desc}</p>
          <div class="pt-2 border-t border-slate-800 text-[11px] font-mono text-cyan-400 flex items-center gap-1">
            <i data-lucide="scale" class="w-3.5 h-3.5"></i>
            <span>${item.law}</span>
          </div>
        </div>
      `).join('');

      lucide.createIcons();
    }

    function filterPatternLib(cat) {
      document.querySelectorAll('.pattern-filter-btn').forEach(btn => {
        btn.classList.remove('bg-brand-500/20', 'text-brand-400', 'border-brand-500/30');
        btn.classList.add('text-slate-400');
      });
      event.target.classList.add('bg-brand-500/20', 'text-brand-400', 'border-brand-500/30');
      renderPatternDatabase(cat);
    }

    // RENDER AUDIT HISTORY TABLE (TAB 4)
    function renderHistoryTable() {
      const tbody = document.getElementById('history-table-body');
      tbody.innerHTML = auditHistory.map((item, idx) => `
        <tr class="hover:bg-slate-900/60 transition">
          <td class="p-3 font-semibold text-slate-200">${item.domain}</td>
          <td class="p-3 text-slate-400">${item.category}</td>
          <td class="p-3">
            <span class="px-2 py-0.5 rounded text-[11px] font-bold ${item.score > 75 ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'}">
              ${item.score}%
            </span>
          </td>
          <td class="p-3 text-slate-300">${item.pattern}</td>
          <td class="p-3 text-slate-500">${item.date}</td>
          <td class="p-3 text-right">
            <button onclick="viewReportModal(${idx})" class="text-xs px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-brand-400 border border-slate-700">
              Report
            </button>
          </td>
        </tr>
      `).join('');
    }

    function filterHistoryTable() {
      const query = document.getElementById('history-search-input').value.toLowerCase();
      const rows = document.querySelectorAll('#history-table-body tr');
      rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
      });
    }

    // MODAL REPORT EXPORT
    function viewReportModal(idx) {
      const item = auditHistory[idx] || auditHistory[0];
      const modal = document.getElementById('report-modal');
      const content = document.getElementById('modal-report-content');

      content.innerText = `=====================================================
SENTINELSHIELD AUDIT REPORT - LEGAL COMPLIANCE
=====================================================
Target Domain: ${item.domain}
Audit Timestamp: ${item.date}
Scam Risk Assessment: ${item.score}% (CRITICAL THREAT)
Primary Violation: ${item.pattern}

EXECUTIVE AUDIT SUMMARY:
SentinelShield autonomous web agent traversed the contract document and checkout flow.
Identified severe consumer right violations, non-consensual payment clauses, and misleading UI dark patterns.

RECOMMENDED LEGAL DIRECTIVES:
1. Revoke UPI e-Mandates under Reserve Bank of India Fair Practice Directives.
2. Submit domain report to National Cyber Crime Reporting Portal.
3. Utilize SentinelShield automated revocation template for formal communication.

-----------------------------------------------------
Certified by SentinelShield AI Agent v2.4
=====================================================`;

      modal.classList.remove('hidden');
    }

    function exportAuditPDF() {
      viewReportModal(0);
    }

    function closeModal() {
      document.getElementById('report-modal').classList.add('hidden');
    }

    // INIT ON LOAD
    window.onload = function() {
      lucide.createIcons();
    };
  </script>
</body>
</html># Rasmalai
