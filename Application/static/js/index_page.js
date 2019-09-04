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
  changeButtonColumnName();
};


main();
