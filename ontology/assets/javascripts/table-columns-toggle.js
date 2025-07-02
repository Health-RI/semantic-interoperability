function initColumnToggles() {
  const table = document.querySelector('table');
  const toggleContainer = document.getElementById('columnToggles');

  if (!table || !toggleContainer) return;

  // Prevent double initialization on repeated SPA navigations
  if (toggleContainer.dataset.initialized) return;
  toggleContainer.dataset.initialized = 'true';

  const headers = table.querySelectorAll('thead th');
  if (!headers.length) return;

  // DEFINE WHICH HEADER NAMES YOU WANT VISIBLE BY DEFAULT
  const defaultVisible = ['subject_id', 'predicate_id', 'object_id'];

  // Clear existing toggles
  toggleContainer.innerHTML = '';

  // Add bulk controls
  const bulkControls = document.createElement('div');
  bulkControls.style.marginBottom = '8px';

  const makeButton = (text) => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = text;
    btn.classList.add('column-toggle-button');
    return btn;
  };

  const checkAllBtn = makeButton('Check all');
  const uncheckAllBtn = makeButton('Uncheck all');
  const checkDefaultBtn = makeButton('Check most common');

  bulkControls.appendChild(checkAllBtn);
  bulkControls.appendChild(uncheckAllBtn);
  bulkControls.appendChild(checkDefaultBtn);
  toggleContainer.parentNode.insertBefore(bulkControls, toggleContainer);

  // Create and store all checkbox references
  const checkboxRefs = [];

  headers.forEach((th, index) => {
    const headerText = th.textContent.trim();

    const label = document.createElement('label');
    label.style.marginRight = '10px';

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.dataset.colIndex = index;

    // Check if header is in defaultVisible
    const isVisibleByDefault = defaultVisible.includes(headerText);
    checkbox.checked = isVisibleByDefault;

    // Initially hide columns not in defaultVisible
    if (!isVisibleByDefault) {
      table.querySelectorAll('tr').forEach(row => {
        const cells = row.querySelectorAll('th, td');
        if (cells[index]) {
          cells[index].style.display = 'none';
        }
      });
    }

    // Add behavior on change
    checkbox.addEventListener('change', function() {
      const colIndex = parseInt(this.dataset.colIndex);
      const show = this.checked;

      table.querySelectorAll('tr').forEach(row => {
        const cells = row.querySelectorAll('th, td');
        if (cells[colIndex]) {
          cells[colIndex].style.display = show ? '' : 'none';
        }
      });
    });

    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(' ' + headerText));
    toggleContainer.appendChild(label);

    checkboxRefs.push({ checkbox, headerText });
  });

  // Add event listeners for bulk buttons
  checkAllBtn.addEventListener('click', () => {
    checkboxRefs.forEach(ref => {
      if (!ref.checkbox.checked) ref.checkbox.click();
    });
  });

  uncheckAllBtn.addEventListener('click', () => {
    checkboxRefs.forEach(ref => {
      if (ref.checkbox.checked) ref.checkbox.click();
    });
  });

  checkDefaultBtn.addEventListener('click', () => {
    checkboxRefs.forEach(ref => {
      const shouldCheck = defaultVisible.includes(ref.headerText);
      if (ref.checkbox.checked !== shouldCheck) {
        ref.checkbox.click();
      }
    });
  });
}

if (typeof document$ !== 'undefined') {
  document$.subscribe(() => {
    initColumnToggles();
  });
} else {
  document.addEventListener('DOMContentLoaded', initColumnToggles);
}
