const checkPasswords = () => {
  let firstPassword = document.getElementById('password');
  let secondPassword = document.getElementById('re_password');
  let log = document.getElementById('log');
  if (!(firstPassword.value) || firstPassword.value !== '') {
    if (!(secondPassword.value) || secondPassword.value !== '') {
      if (firstPassword.value != secondPassword.value) {
        log.style.display = 'block';
        log.innerHTML = 'Passwords do not match.';
      } else {
        log.style.display = 'none';
      }
    }
  }
};


const main = () => {
  const secondPasswordInput = document.getElementById('re_password');
  secondPasswordInput.oninput = checkPasswords;
};


main();
