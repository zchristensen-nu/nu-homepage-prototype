/* Lab notebook: figure numbers and the research caption */
/* figures are numbered in reading order, counting only those on the page (a news row that
   did not load has no figure, so the numbers never skip) */
window.numberFigs = () => {
  let n = 0;
  $$("[data-fig]").forEach(f => {
    if (f.closest("[hidden]")) return;
    n++;
    const t = f.querySelector(".fig-n");
    if (t) t.textContent = "Fig. " + n;
  });
};
numberFigs();
/* the research figure's caption names its panels; the open panel reads in ink */
{
  const cards = $$(".xcard"), capL = $("#xcapL");
  if (capL) {
    capL.innerHTML = cards.map((c, k) => `<span class="xp" data-k="${k}"><b>${"abcde"[k]}</b> ${c.querySelector(".xtag").textContent}</span>`).join("");
    const sync = () => cards.forEach((c, k) => capL.children[k].classList.toggle("on", c.classList.contains("active")));
    cards.forEach(c => { c.addEventListener("click", sync); c.addEventListener("keydown", () => setTimeout(sync)); });
    sync();
  }
}
