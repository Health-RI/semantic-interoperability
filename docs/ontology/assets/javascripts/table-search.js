function initTableSearch() {
  const searchInput = document.getElementById('tableSearchInput');
  if (!searchInput) return;

  // Prevent duplicate event handlers
  if (searchInput.dataset.initialized) return;
  searchInput.dataset.initialized = 'true';

  searchInput.addEventListener('input', function() {
    const filter = searchInput.value.toLowerCase();
    document.querySelectorAll('table tbody tr').forEach(function(row) {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(filter) ? '' : 'none';
    });
  });
}

if (typeof document$ !== 'undefined') {
  document$.subscribe(() => {
    initTableSearch();
  });
} else {
  document.addEventListener('DOMContentLoaded', initTableSearch);
}
