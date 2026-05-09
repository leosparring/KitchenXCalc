(function(){
  const LS_KEY = 'kxappliances_autosave';
  const LANG_KEY = 'kxappliances_language';
  const MAX_SLOTS = 8;
  const SLOT_FIELDS = ['appliance','width','depth','dia','drip','qty'];

  // ── Save state to localStorage ──────────────────────────────────
  function saveState(){
    try {
      const data = { slots: [], timestamp: Date.now() };
      // Find active slots by checking which selects exist and have a value
      for(let i = 1; i <= MAX_SLOTS; i++){
        const sel = document.getElementById('appliance' + i);
        if(!sel) continue;
        const slot = { id: i };
        SLOT_FIELDS.forEach(function(f){
          const el = document.getElementById(f + i);
          if(el) slot[f] = el.value;
        });
        data.slots.push(slot);
      }
      localStorage.setItem(LS_KEY, JSON.stringify(data));
      const langSelect = document.getElementById('language');
      if (langSelect) {
        localStorage.setItem(LANG_KEY, langSelect.value);
      }
    } catch(e){}
  }

  function restoreLanguage(){
    try {
      const lang = localStorage.getItem(LANG_KEY);
      const langSelect = document.getElementById('language');
      if (lang && langSelect) {
        langSelect.value = lang;
        langSelect.dispatchEvent(new Event('change', {bubbles: true}));
      }
    } catch(e){}
  }

  // ── Restore state from localStorage ────────────────────────────
  function restoreState(){
    try {
      const raw = localStorage.getItem(LS_KEY);
      if(!raw) return;
      const data = JSON.parse(raw);
      if(!data.slots || !data.slots.length) return;

      // Click "Add Another Hazard" to create enough slots
      const firstSlot = data.slots[0];
      const addBtn = document.querySelector('.btn-add');

      function setField(id, value){
        const el = document.getElementById(id);
        if(!el || value === undefined || value === null || value === '') return;
        const nativeInputSetter = Object.getOwnPropertyDescriptor(
          window.HTMLInputElement.prototype, 'value') ||
          Object.getOwnPropertyDescriptor(window.HTMLSelectElement.prototype, 'value');
        if(nativeInputSetter && nativeInputSetter.set){
          nativeInputSetter.set.call(el, value);
        } else {
          el.value = value;
        }
        el.dispatchEvent(new Event('change', {bubbles: true}));
        el.dispatchEvent(new Event('input', {bubbles: true}));
      }

      function restoreSlot(slot, attempt){
        attempt = attempt || 0;
        if(attempt > 30) return;
        const appSel = document.getElementById('appliance' + slot.id);
        if(!appSel){
          // Slot not rendered yet — click Add button and retry
          if(addBtn && slot.id > 1) addBtn.click();
          setTimeout(function(){ restoreSlot(slot, attempt + 1); }, 150);
          return;
        }
        // Set appliance selector
        setField('appliance' + slot.id, slot.appliance);
        // Wait for dynamic inputs to render, then set dimensions
        setTimeout(function(){
          SLOT_FIELDS.forEach(function(f){
            if(f !== 'appliance') setField(f + slot.id, slot[f]);
          });
        }, 300);
      }

      // Restore slots sequentially with delays to allow Shiny to render
      data.slots.forEach(function(slot, idx){
        setTimeout(function(){ restoreSlot(slot, 0); }, idx * 500);
      });

    } catch(e){}
  }

  // Auto-save on any input change (debounced)
  let saveTimer = null;
  function closeLanguageDropdown(){
    const picker = document.getElementById('language_picker');
    if(picker) picker.classList.remove('open');
  }

  window.selectLanguage = function(lang){
    const langSelect = document.getElementById('language');
    if(!langSelect) return;
    langSelect.value = lang;
    langSelect.dispatchEvent(new Event('change', {bubbles: true}));
    closeLanguageDropdown();
  };

  document.addEventListener('click', function(event){
    const picker = document.getElementById('language_picker');
    if(!picker) return;
    if(picker.contains(event.target)) return;
    closeLanguageDropdown();
  });

  document.addEventListener('change', function(event){ 
    if(event.target && event.target.id === 'language'){
      closeLanguageDropdown();
    }
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveState, 800);
  });
  document.addEventListener('input', function(){
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveState, 800);
  });

  // Restore on page load after Shiny is ready
  if(window.Shiny){
    Shiny.addCustomMessageHandler('__kx_ready__', function(){ restoreLanguage(); restoreState(); });
  }
  // Fallback: restore after a delay
  setTimeout(function(){ restoreLanguage(); restoreState(); }, 1500);
})();
