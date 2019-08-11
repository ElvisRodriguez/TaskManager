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

const changeButtonColumnName = () => {
  const tags = document.getElementsByTagName('th');
  for (let i = 0; i < tags.length; i++) {
    if (tags[i].innerText == 'Clear Task') {
      tags[i].innerText = 'Options';
      break;
    }
  }
}


const main = () => {
  let date = document.getElementById("date");
  getCurrentDate(date);
  changeButtonColumnName();
};


main();
