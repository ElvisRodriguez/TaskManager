const redirectToSignup = () => {
  location.href='/signup';
};

const redirectButton = document.getElementById('redirect_button');
redirectButton.onclick = redirectToSignup;
