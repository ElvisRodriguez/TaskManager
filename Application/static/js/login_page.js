const redirectToSignup = () => {
  location.href = '/signup';
};


const main = () => {
  const redirectButton = document.getElementById('redirect_button');
  redirectButton.onclick = redirectToSignup;
};


main();
