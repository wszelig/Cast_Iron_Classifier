// Get references to the filter inputs and the table body
const typeFilter = document.getElementById("type-filter");
const nameFilter = document.getElementById("name-filter");
const dimensionsFilter = document.getElementById("dimensions-filter");
const dateFilter = document.getElementById("date-filter");
const tableBody = document.getElementsByTagName("tbody")[0];

// Attach event listeners to the filter inputs
typeFilter.addEventListener("change", applyFilters);
nameFilter.addEventListener("input", applyFilters);
dimensionsFilter.addEventListener("input", applyFilters);
dateFilter.addEventListener("change", applyFilters);

// Define the filter function
function applyFilters() {
  // Get the filter values
  const typeValue = typeFilter.value.toLowerCase();
  const nameValue = nameFilter.value.toLowerCase();
  const dimensionsValue = dimensionsFilter.value.toLowerCase();
  const dateValue = dateFilter.value;

  // Loop through the table rows and hide/show them based on the filters
  for (let row of tableBody.rows) {
    const typeCell = row.cells[1].textContent.toLowerCase();
    const nameCell = row.cells[2].textContent.toLowerCase();
    const dimensionsCell = row.cells[3].textContent.toLowerCase();
    const dateCell = row.cells[4].textContent.substring(0, 10);

    if (
      (typeValue === "" || typeCell.includes(typeValue)) &&
      (nameValue === "" || nameCell.includes(nameValue)) &&
      (dimensionsValue === "" || dimensionsCell.includes(dimensionsValue)) &&
      (dateValue === "" || dateCell === dateValue)
    ) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  }
}