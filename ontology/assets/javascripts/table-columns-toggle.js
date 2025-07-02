document.addEventListener('DOMContentLoaded', function() {
  const table = document.querySelector('table');
  const toggleContainer = document.getElementById('columnToggles');
  if (!table || !toggleContainer) return;

  const headers = table.querySelectorAll('thead th');
  if (!headers.length) return;

  // DEFINE WHICH HEADER NAMES YOU WANT VISIBLE BY DEFAULT
  const defaultVisible = ['subject_id', 'predicate_id', 'object_id'];

  // Clear existing toggles
  toggleContainer.innerHTML = '';

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
  });
});
