const otpBoxes = [...document.querySelectorAll('[data-otp] input')];
otpBoxes.forEach((box, i) => {
  box.addEventListener('input', () => {
    box.value = box.value.replace(/\D/g, '').slice(-1);
    if (box.value && i < otpBoxes.length - 1) otpBoxes[i + 1].focus();
  });
  box.addEventListener('keydown', e => {
    if (e.key === 'Backspace' && !box.value && i > 0) otpBoxes[i - 1].focus();
    if (e.key === 'ArrowLeft' && i > 0) otpBoxes[i - 1].focus();
    if (e.key === 'ArrowRight' && i < otpBoxes.length - 1) otpBoxes[i + 1].focus();
  });
  box.addEventListener('paste', e => {
    e.preventDefault();
    const text = (e.clipboardData.getData('text') || '').replace(/\D/g, '');
    text.split('').slice(0, otpBoxes.length - i).forEach((ch, j) => { otpBoxes[i + j].value = ch; });
    otpBoxes[Math.min(i + text.length, otpBoxes.length - 1)].focus();
  });
});
