document.addEventListener("DOMContentLoaded", function () {
  const flippableCards = document.querySelectorAll(".flippable-card");

  flippableCards.forEach((card) => {
    let isFlipped = false;

    card.addEventListener("click", () => {
      if (isFlipped) {
        card.classList.remove("flipped");
      } else {
        card.classList.add("flipped");
      }
      isFlipped = !isFlipped;
    });
  });
});
