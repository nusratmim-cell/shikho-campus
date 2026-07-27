(() => {
  const nav = document.querySelector("nav");
  if (!nav) return;

  const iconFor = (title) => {
    const value = title.toLowerCase();
    if (/on this page|start here/.test(value)) return "⌂";
    if (/learning|course|content|teaching|devices/.test(value)) return "◇";
    if (/marks|exam|assessment|result|grading|features/.test(value)) return "✓";
    if (/money|fee|payment/.test(value)) return "৳";
    if (/advis|campus|support/.test(value)) return "?";
    if (/modules|go to/.test(value)) return "↗";
    if (/more pages|resources/.test(value)) return "··";
    if (/ai|campus ai/.test(value)) return "✦";
    return "·";
  };

  const aliases = {
    pay: ["fee", "fees", "payment", "bkash", "money", "dues", "installment"],
    fee: ["pay", "payment", "money", "dues"],
    mark: ["grade", "grades", "grading", "result", "results"],
    grade: ["mark", "marks", "grading", "result"],
    class: ["live", "lecture", "course", "attendance"],
    attend: ["attendance", "eligibility", "absent"],
    ai: ["tutor", "assistant", "copilot", "analyst", "practice", "smart class"],
    advisor: ["advising", "advise", "degree plan"],
    hold: ["block", "library", "dues"],
    certify: ["certification", "approve", "final"],
    phone: ["mobile", "responsive", "device", "tv", "laptop"],
    mobile: ["phone", "app", "responsive", "device"],
    tv: ["smart tv", "television", "screen", "responsive", "device"],
    laptop: ["desktop", "web", "responsive", "device"],
  };

  const expandQuery = (query) => {
    const parts = query.split(/\s+/).filter(Boolean);
    const terms = new Set(parts);
    parts.forEach((part) => {
      Object.entries(aliases).forEach(([key, values]) => {
        if (part.includes(key) || key.includes(part)) {
          terms.add(key);
          values.forEach((value) => terms.add(value));
        }
      });
    });
    return [...terms];
  };

  const textMatches = (haystack, terms) => {
    const value = haystack.toLowerCase();
    return terms.some((term) => value.includes(term));
  };

  const currentFile = location.pathname.split("/").pop() || "index.html";
  const currentHash = location.hash;

  // ---- Document map: Overview is always first ----
  // Order: 1 Overview (home) → 2 Modules → 3 Supporting pages → 4 References → 5 Our demo
  const MODULES = [
    { file: "student.html", label: "Student", initial: "S", tone: "student" },
    { file: "faculty.html", label: "Faculty", initial: "F", tone: "faculty" },
    { file: "admin.html", label: "Administrator", initial: "A", tone: "admin" },
    { file: "coordinator.html", label: "Coordinator", initial: "C", tone: "coordinator" },
  ];

  const SUPPORT_PAGES = [
    { file: "wireframes.html", label: "Reference wireframes" },
    { file: "build.html", label: "UI & engineering build" },
    { file: "ai.html", label: "Campus AI" },
    { file: "platform.html", label: "How parts connect" },
    { file: "university-activities.html", label: "All university activities" },
  ];

  const REFERENCES = [
    {
      href: "https://youtu.be/IgHHeRYEqZM?si=UX2wM4qJGZ2c0JCX",
      label: "Docebo LMS tour",
      note: "Live university LMS",
    },
    {
      href: "https://youtu.be/dwXwah-feFk?si=LHTlSJqGjqkOSzqj",
      label: "Canvas 101",
      note: "University LMS overview",
    },
    {
      href: "https://youtu.be/IJIP0XCy9s0?si=KiELhbY7d-MMGDhl",
      label: "Canvas for teachers",
      note: "Setup to publishing",
    },
  ];

  const ALL_PAGES = [
    { file: "index.html", label: "Overview" },
    ...MODULES,
    ...SUPPORT_PAGES,
  ];
  const MODULE_FILES = MODULES.map((module) => module.file);
  const currentLabel =
    ALL_PAGES.find((page) => page.file === currentFile)?.label || "Menu";

  // Brand always returns to Overview
  const brand = nav.querySelector(".brand");
  if (brand && !brand.closest("a")) {
    const brandLink = document.createElement("a");
    brandLink.href = "./index.html";
    brandLink.className = "nav-brand-link";
    brandLink.setAttribute("aria-label", "Overview — start here");
    brand.replaceWith(brandLink);
    brandLink.append(brand);
  }

  const map = document.createElement("div");
  map.className = "nav-map";

  // 1. Overview — the start of everything
  const home = document.createElement("a");
  home.className = "nav-home";
  home.href = "./index.html";
  if (currentFile === "index.html") {
    home.classList.add("is-active");
    home.setAttribute("aria-current", "page");
  }
  home.innerHTML =
    '<span class="nav-home-mark" aria-hidden="true">1</span>' +
    '<span class="nav-home-copy"><strong>Overview</strong><em>Start here</em></span>';

  // 2. Modules
  const modBlock = document.createElement("div");
  modBlock.className = "nav-map-block";
  const modLabel = document.createElement("div");
  modLabel.className = "nav-map-label";
  modLabel.textContent = "2 · Modules";
  const grid = document.createElement("div");
  grid.className = "nav-switcher-grid";
  MODULES.forEach((module) => {
    const item = document.createElement("a");
    item.className = `mod-chip tone-${module.tone}`;
    item.href = `./${module.file}`;
    if (module.file === currentFile) {
      item.classList.add("is-active");
      item.setAttribute("aria-current", "page");
    }
    item.innerHTML = `<span class="mod-initial" aria-hidden="true">${module.initial}</span><span class="mod-name">${module.label}</span>`;
    grid.append(item);
  });
  modBlock.append(modLabel, grid);

  // 3. Supporting pages
  const supportBlock = document.createElement("div");
  supportBlock.className = "nav-map-block";
  const supportLabel = document.createElement("div");
  supportLabel.className = "nav-map-label";
  supportLabel.textContent = "3 · Also in this document";
  const supportList = document.createElement("div");
  supportList.className = "nav-support-list";
  SUPPORT_PAGES.forEach((page) => {
    const item = document.createElement("a");
    item.href = `./${page.file}`;
    item.textContent = page.label;
    if (page.file === currentFile) {
      item.classList.add("is-active");
      item.setAttribute("aria-current", "page");
    }
    supportList.append(item);
  });
  supportBlock.append(supportLabel, supportList);

  // 4. Reference LMS videos
  const refBlock = document.createElement("div");
  refBlock.className = "nav-map-block";
  const refLabel = document.createElement("div");
  refLabel.className = "nav-map-label";
  refLabel.textContent = "4 · See a live university LMS";
  const refList = document.createElement("div");
  refList.className = "nav-ref-list";
  REFERENCES.forEach((ref) => {
    const item = document.createElement("a");
    item.href = ref.href;
    item.target = "_blank";
    item.rel = "noopener";
    item.innerHTML = `<span class="nav-ref-title">${ref.label}</span><span class="nav-ref-note">${ref.note}</span>`;
    refList.append(item);
  });
  refBlock.append(refLabel, refList);

  // 5. Our working demo
  const demo = document.createElement("a");
  demo.className = "nav-switcher-demo";
  demo.href = "https://shikho-brac-platform.vercel.app/";
  demo.target = "_blank";
  demo.rel = "noopener";
  demo.textContent = "5 · Open our live demo ↗";

  map.append(home, modBlock, supportBlock, refBlock, demo);
  nav.querySelector(".sub")?.insertAdjacentElement("afterend", map);

  // Remove now-duplicated page links from the authored menu
  const mapFiles = new Set([
    "index.html",
    ...MODULES.map((module) => module.file),
    ...SUPPORT_PAGES.map((page) => page.file),
  ]);
  nav.querySelectorAll(":scope > a").forEach((link) => {
    if (link.classList.contains("nav-brand-link")) return;
    if (link.closest(".nav-map")) return;
    const url = new URL(link.href, location.href);
    const file = url.pathname.split("/").pop();
    const isDemo = url.hostname.includes("vercel.app");
    const isYouTube = /youtu\.?be/.test(url.hostname);
    if (!url.hash && (mapFiles.has(file) || isDemo || isYouTube)) link.remove();
  });

  const headings = [...nav.querySelectorAll(":scope > .g")];

  headings.forEach((heading, index) => {
    const section = document.createElement("details");
    section.className = "nav-section";

    const titleText = heading.textContent.trim();
    const summary = document.createElement("summary");
    const icon = document.createElement("span");
    icon.className = "nav-group-icon";
    icon.setAttribute("aria-hidden", "true");
    icon.textContent = iconFor(titleText);
    const title = document.createElement("span");
    title.textContent = titleText;
    summary.append(icon, title);

    const links = document.createElement("div");
    links.className = "nav-section-links";

    let node = heading.nextElementSibling;
    while (node && !node.classList.contains("g")) {
      const next = node.nextElementSibling;
      if (node.matches("a")) links.append(node);
      node = next;
    }

    heading.replaceWith(section);
    section.append(summary, links);

    // Drop groups emptied by the module switcher
    if (!links.querySelector("a")) {
      section.remove();
      return;
    }

    if (
      index === 0 ||
      /on this page|go to|modules|resources|more pages/i.test(titleText)
    ) {
      section.open = true;
    }
  });

  const sections = [...nav.querySelectorAll(".nav-section")];
  if (sections.length && !sections.some((section) => section.open)) {
    sections[0].open = true;
  }

  // A clear divider so the document map above reads differently from the page TOC below.
  const firstSection = sections[0];
  if (firstSection) {
    const firstTitleEl = firstSection.querySelector("summary span:last-child");
    const firstTitle = (firstTitleEl?.textContent || "").trim().toLowerCase();
    const isModulePage = MODULE_FILES.includes(currentFile);
    if (isModulePage) {
      if (firstTitle === "on this page" && firstTitleEl) firstTitleEl.textContent = "Introduction";
      const label = document.createElement("div");
      label.className = "nav-region-label";
      label.textContent = "On this page";
      firstSection.before(label);
    } else if (firstTitle !== "on this page") {
      const label = document.createElement("div");
      label.className = "nav-region-label";
      label.textContent = "On this page";
      firstSection.before(label);
    }
  }

  const links = [...nav.querySelectorAll(".nav-section-links a")];
  links.forEach((link) => {
    const url = new URL(link.href, location.href);
    const linkFile = url.pathname.split("/").pop() || "index.html";
    const samePage = linkFile === currentFile;
    const exactHash = url.hash && url.hash === currentHash;
    const pageOnly = samePage && !url.hash && !currentHash;
    const isOverview =
      currentFile !== "index.html" &&
      linkFile === "index.html" &&
      !url.hash &&
      /overview/i.test(link.textContent);

    if (exactHash || pageOnly) {
      link.classList.add("is-current");
      link.closest("details").open = true;
      link.setAttribute("aria-current", "location");
    }
    if (isOverview) link.classList.add("nav-home-link");

    // Index page content for better search (ids + nearby headings)
    const hash = url.hash.replace(/^#/, "");
    let pageHint = "";
    if (hash) {
      const target = document.getElementById(hash);
      if (target) {
        pageHint = [
          hash,
          target.textContent,
          target.querySelector("h2,h3,.intent")?.textContent || "",
        ].join(" ");
      }
    }
    link.dataset.searchText = [
      link.textContent,
      hash,
      link.getAttribute("href") || "",
      pageHint,
    ]
      .join(" ")
      .toLowerCase()
      .replace(/\s+/g, " ")
      .trim();
  });

  const searchWrap = document.createElement("div");
  searchWrap.className = "nav-search-wrap";

  const search = document.createElement("input");
  search.className = "nav-search";
  search.type = "search";
  search.placeholder = "Search this page…";
  search.setAttribute("aria-label", "Search this page");
  search.setAttribute("autocomplete", "off");
  search.setAttribute("spellcheck", "false");

  const searchMeta = document.createElement("div");
  searchMeta.className = "nav-search-meta";
  searchMeta.hidden = true;

  searchWrap.append(search, searchMeta);
  map.insertAdjacentElement("afterend", searchWrap);

  const empty = document.createElement("div");
  empty.className = "nav-empty";
  empty.textContent = "Nothing matched. Try fees, grades, attendance, AI, or devices.";
  nav.append(empty);

  let lastMatches = [];

  const clearMarks = () => {
    document.querySelectorAll(".search-hit").forEach((el) => el.classList.remove("search-hit"));
  };

  const runSearch = (jumpToFirst = false) => {
    const query = search.value.trim().toLowerCase();
    clearMarks();
    lastMatches = [];

    if (!query) {
      nav.querySelectorAll(".nav-section").forEach((section) => {
        section.hidden = false;
        section.classList.remove("is-search-hit");
        section.querySelectorAll("a").forEach((link) => {
          link.hidden = false;
          link.classList.remove("is-search-match");
        });
      });
      empty.classList.remove("is-visible");
      searchMeta.hidden = true;
      searchMeta.textContent = "";
      return;
    }

    const terms = expandQuery(query);
    let matchCount = 0;

    nav.querySelectorAll(".nav-section").forEach((section) => {
      const summaryText = section.querySelector("summary").textContent.toLowerCase();
      const sectionTitleHit = textMatches(summaryText, terms);
      let sectionHasLinkHit = false;

      section.querySelectorAll("a").forEach((link) => {
        const haystack = link.dataset.searchText || link.textContent.toLowerCase();
        const hit = textMatches(haystack, terms) || sectionTitleHit;
        link.hidden = !hit;
        link.classList.toggle("is-search-match", hit && textMatches(haystack, terms));
        if (hit) {
          matchCount += 1;
          sectionHasLinkHit = true;
          lastMatches.push(link);
          const hash = new URL(link.href, location.href).hash.replace(/^#/, "");
          if (hash) document.getElementById(hash)?.classList.add("search-hit");
        }
      });

      const showSection = sectionTitleHit || sectionHasLinkHit;
      section.hidden = !showSection;
      section.classList.toggle("is-search-hit", showSection);
      if (showSection) section.open = true;
    });

    empty.classList.toggle("is-visible", matchCount === 0);
    searchMeta.hidden = false;
    searchMeta.textContent =
      matchCount === 0
        ? "0 matches"
        : matchCount === 1
          ? "1 match · Enter to open"
          : `${matchCount} matches · Enter to open first`;

    if (jumpToFirst && lastMatches[0]) {
      lastMatches[0].click();
      lastMatches[0].focus();
    }
  };

  search.addEventListener("input", () => runSearch(false));
  search.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      runSearch(true);
    }
    if (event.key === "Escape") {
      search.value = "";
      runSearch(false);
      search.blur();
    }
  });

  const button = document.createElement("button");
  button.className = "nav-menu-button";
  button.type = "button";
  button.setAttribute("aria-label", "Open contents menu");
  button.setAttribute("aria-expanded", "false");
  button.innerHTML = `<span class="bars" aria-hidden="true">☰</span><span>${currentLabel}</span>`;

  const overlay = document.createElement("div");
  overlay.className = "nav-overlay";

  const setOpen = (open) => {
    document.body.classList.toggle("nav-open", open);
    button.setAttribute("aria-expanded", String(open));
    button.querySelector(".bars").textContent = open ? "✕" : "☰";
    button.querySelector("span:last-child").textContent = open ? "Close" : currentLabel;
    if (open) setTimeout(() => search.focus(), 180);
  };

  const navClose = document.createElement("button");
  navClose.type = "button";
  navClose.className = "nav-close";
  navClose.setAttribute("aria-label", "Close menu");
  navClose.innerHTML = '<span aria-hidden="true">✕</span>';
  navClose.addEventListener("click", () => setOpen(false));
  nav.prepend(navClose);

  button.addEventListener("click", () => setOpen(!document.body.classList.contains("nav-open")));
  overlay.addEventListener("click", () => setOpen(false));
  nav.addEventListener("click", (event) => {
    if (event.target.closest("a") && matchMedia("(max-width: 820px)").matches) setOpen(false);
  });
  addEventListener("keydown", (event) => {
    if (event.key === "Escape") setOpen(false);
    // "/" focuses search when not typing in an input
    if (
      event.key === "/" &&
      !event.metaKey &&
      !event.ctrlKey &&
      !/^(INPUT|TEXTAREA|SELECT)$/.test(event.target.tagName)
    ) {
      event.preventDefault();
      if (matchMedia("(max-width: 820px)").matches) setOpen(true);
      search.focus();
      search.select();
    }
  });
  addEventListener("hashchange", () => {
    links.forEach((link) => {
      const active = new URL(link.href, location.href).hash === location.hash;
      link.classList.toggle("is-current", active);
      if (active) link.closest("details").open = true;
    });
  });

  document.body.append(overlay, button);

  // Wide reference tables scroll sideways instead of pushing the page out on phones
  document.querySelectorAll("main table").forEach((table) => {
    if (table.parentElement?.classList.contains("table-scroll")) return;
    const wrap = document.createElement("div");
    wrap.className = "table-scroll";
    table.replaceWith(wrap);
    wrap.append(table);
  });

  // ---- Reading progress + scroll spy: always show where the reader is ----
  const progress = document.createElement("div");
  progress.className = "read-progress";
  document.body.append(progress);

  const spyItems = links
    .map((link) => {
      const url = new URL(link.href, location.href);
      const file = url.pathname.split("/").pop() || "index.html";
      const id = url.hash.replace(/^#/, "");
      if (!id || file !== currentFile) return null;
      const target = document.getElementById(id);
      return target ? { link, target } : null;
    })
    .filter(Boolean);

  spyItems.sort((a, b) =>
    a.target.compareDocumentPosition(b.target) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1
  );

  let activeLink = null;
  const setActive = (link) => {
    if (link === activeLink) return;
    spyItems.forEach((item) => item.link.classList.remove("is-reading", "is-current"));
    activeLink = link;
    if (!link) return;
    link.classList.add("is-reading");
    const section = link.closest("details");
    if (section && !section.open) section.open = true;
    if (!matchMedia("(max-width: 820px)").matches) {
      const rect = link.getBoundingClientRect();
      if (rect.top < 80 || rect.bottom > innerHeight - 16) {
        link.scrollIntoView({ block: "center", behavior: "auto" });
      }
    }
  };

  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      const doc = document.documentElement;
      const max = doc.scrollHeight - innerHeight;
      progress.style.width = max > 0 ? `${Math.min(100, (doc.scrollTop / max) * 100)}%` : "0";

      if (!spyItems.length) return;
      const line = 132;
      let current = null;
      for (const item of spyItems) {
        if (item.target.getBoundingClientRect().top - line <= 0) current = item.link;
        else break;
      }
      if (!current && doc.scrollTop < 40) current = spyItems[0].link;
      if (current) setActive(current);
    });
  };
  addEventListener("scroll", onScroll, { passive: true });
  addEventListener("resize", onScroll, { passive: true });
  onScroll();
})();
