function initTableSort() {
  document.querySelectorAll('table').forEach(function(table) {
    if (!table.dataset.tablesortInitialized) {
      new Tablesort(table);
      table.dataset.tablesortInitialized = 'true';
    }
  });
}

if (typeof document$ !== 'undefined') {
  document$.subscribe(() => {
    initTableSort();
  });
} else {
  document.addEventListener('DOMContentLoaded', initTableSort);
}
