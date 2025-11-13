// ========== Toast Notification System ==========
function showAlert(message, type = "success") {
  const alertBox = document.createElement("div");
  alertBox.className = `
    fixed top-6 right-6 z-50 px-4 py-2 rounded shadow-lg transition-opacity duration-500
    ${type === "error" ? "bg-red-500" : "bg-green-500"}
    text-white text-lg opacity-100 fade-in
  `.replace(/\s+/g, ' ');
  alertBox.innerText = message;
  alertBox.setAttribute('role', 'alert');

  document.body.appendChild(alertBox);
  setTimeout(() => alertBox.classList.add("opacity-0"), 3500);
  setTimeout(() => alertBox.remove(), 4000);
}

// ========== Button Loading Animation ==========
function setLoading(buttonId, loading = true, text = "Loading...") {
  const btn = document.getElementById(buttonId);
  if (!btn) return;
  if (loading) {
    btn.dataset.originalText = btn.innerHTML;
    btn.innerHTML = `<svg class="inline w-5 h-5 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle><path d="M4 12a8 8 0 018-8" stroke="currentColor" stroke-width="4" stroke-linecap="round"></path></svg>${text}`;
    btn.disabled = true;
  } else {
    btn.innerHTML = btn.dataset.originalText || "Submit";
    btn.disabled = false;
  }
}

// ========== Smooth Scroll to Element ==========
function scrollToSection(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
}

// ========== Success Effect for Mark Attendance ==========
function markAttendanceEffect() {
  const btn = document.getElementById("markBtn");
  if (!btn) return;
  btn.classList.add("bg-green-600");
  btn.innerText = "✅ Attendance Marked!";
  setTimeout(() => {
    btn.innerText = "Mark Attendance";
    btn.classList.remove("bg-green-600");
  }, 3000);
}

// ========== Auto Fade Messages ==========
window.addEventListener("load", () => {
  document.querySelectorAll(".alert").forEach((el) => {
    setTimeout(() => el.classList.add("opacity-0"), 3500);
    setTimeout(() => el.remove(), 4000);
  });
});
