const hero = document.getElementById("game-hero");
const obstacle = document.getElementById("game-obstacle");

const score = document.getElementById("game-score");
const gameBox = document.getElementById("game");
const backgroundLayer1 = document.getElementById("bg-layer-1");
const backgroundLayer2 = document.getElementById("bg-layer-2");
const gameOver = document.getElementById("game-end");
const yourScore = document.getElementById("game-end-score");
const yourHighScore = document.getElementById("game-highscore");
const startScreen = document.getElementById("game-start");

const backgroundAudio = new Audio("./sounds/bg.mp3");
backgroundAudio.loop = true;
const jumpAudio = new Audio("./sounds/jump.mp3");
const dogAudio = new Audio("./sounds/dog.mp3");
const catAudio = new Audio("./sounds/cat.mp3");

let gameLoopInterval = 0;
let currentObstacle = "dog";
let metersRun = 0;
let personalBest = localStorage.getItem("highscore") || 0;

const playAudio = (audio) => {
  audio.currentTime = 0;
  audio.play();
};

const startGame = () => {
  gameOver.classList.add("hidden");
  startAnimations();
  hero.classList.add("hero-running");
  startScreen.classList.add("hidden");
  resetScore();
  playAudio(backgroundAudio);
  startGameLoop();
};

const resetScore = () => {
  score.innerText = 0;
};

const jump = () => {
  if (hero.classList.contains("jump-animation")) {
    return false;
  }
  playAudio(jumpAudio);
  hero.classList.add("jump-animation");
  setTimeout(() => {
    hero.classList.remove("jump-animation");
  }, 500);
};

const dieAnimation = () => {
  if (currentObstacle === "dog") {
    playAudio(dogAudio);
  } else {
    playAudio(catAudio);
  }
  hero.classList.add("hero-dies");
  return new Promise((resolve) =>
    setTimeout(() => {
      hero.classList.remove("hero-dies");
      resolve();
    }, 800)
  );
};

const startAnimations = () => {
  backgroundLayer1.classList.add("bg-animation-layer-1");
  backgroundLayer2.classList.add("bg-animation-layer-2");
  obstacle.classList.add(`obstacle-animation-${currentObstacle}`);
};

const stopAnimations = () => {
  backgroundLayer1.classList.remove("bg-animation-layer-1");
  backgroundLayer2.classList.remove("bg-animation-layer-2");
  hero.classList.remove("hero-running");
  obstacle.classList.remove("obstacle-animation");
  obstacle.classList.remove("obstacle-animation-dog");
  obstacle.classList.remove("obstacle-animation-cat");
};

const stopGame = async () => {
  unregisterListener();
  gameLoopInterval = clearInterval(gameLoopInterval);
  stopAnimations();
  gameOver.classList.remove("hidden");
  yourScore.innerText = score.innerText;
  if (metersRun > personalBest) {
    personalBest = metersRun;
    localStorage.setItem("highscore", personalBest);
  }
  yourHighScore.innerHTML = personalBest;
  await dieAnimation();
  backgroundAudio.pause();
  startScreen.classList.remove("hidden");
  registerListener();
};

// 50% chance for either dog or cat
const toggleObstacleByRandom = () => {
  currentObstacle = Math.random() < 0.5 ? "cat" : "dog";
  if (currentObstacle === "dog") {
    obstacle.classList.remove("obstacle-cat");
    obstacle.classList.add("obstacle-dog");
  } else {
    obstacle.classList.remove("obstacle-dog");
    obstacle.classList.add("obstacle-cat");
  }
};

const getObstacleSpeed = () => {
  // Base speed is between 1 to 4 seconds
  let speed = Math.random() * 3 + 1;
  let additionalSpeed = Math.floor(metersRun / 100) * 0.1;
  speed = Math.max(speed - additionalSpeed, 0.5);
  return speed;
};

const startGameLoop = () => {
  metersRun = 0;
  gameLoopInterval = window.setInterval(() => {
    const heroTop = parseInt(
      window.getComputedStyle(hero).getPropertyValue("top")
    );
    const obstacleLeft = parseInt(
      window.getComputedStyle(obstacle).getPropertyValue("left")
    );
    metersRun += 0.01 * 50; // calculates average human runner speed
    score.innerText = metersRun.toFixed(0) + "m";
    if (obstacleLeft < 0) {
      toggleObstacleByRandom();
      obstacle.classList.add("hidden");
      const randomObstacleSpeed = getObstacleSpeed();
      obstacle.style.animation = `obstacle-${currentObstacle} ${randomObstacleSpeed}s infinite linear`;
    } else {
      obstacle.classList.remove("hidden");
    }

    if (obstacleLeft < 50 && obstacleLeft > 0 && heroTop > 150) {
      obstacle.classList.add("hidden");
      stopGame();
    }
  }, 50);
};

const registerListener = () => {
  document.addEventListener("keydown", keyDownHandler);
};
const unregisterListener = () => {
  document.removeEventListener("keydown", keyDownHandler);
};
const keyDownHandler = () => {
  if (!gameLoopInterval) {
    startGame();
    return false;
  }
  const isGameRunning = gameLoopInterval > 0;
  const isSpaceKey = event.code === "Space";
  if (isGameRunning && isSpaceKey) {
    jump();
  }
};
registerListener();
