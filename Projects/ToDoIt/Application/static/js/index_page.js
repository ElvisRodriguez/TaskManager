const getCurrentDate = (element) => {
  const today = new Date();

  let month = today.getMonth() + 1;
  let day = today.getDate();
  let year = today.getFullYear();

  if (month < 10) {
      month = '0' + month.toString();
  }
  if (day < 10) {
      day = '0' + day.toString();
  }

  const minDate = year + '-' + month + '-' + day;
  element.setAttribute("placeholder", Date());
  element.setAttribute("min", minDate);
  element.setAttribute("max", "2070-01-01");
};

let date = document.getElementById("date");
getCurrentDate(date);