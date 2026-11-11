const state = { jobs: [], profileText: "" };
const $ = (id) => document.getElementById(id);

function dateLabel(value) {
  if (!value) return "غير متاح";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "غير متاح" : new Intl.DateTimeFormat("ar-EG", { dateStyle: "medium", timeStyle: "short" }).format(date);
}
function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
}
function safeHref(value) {
  try { const url = new URL(value); return url.protocol === "https:" ? escapeHtml(url.href) : "#"; }
  catch { return "#"; }
}
function renderJobs() {
  const query = $("search").value.trim().toLowerCase();
  const platform = $("platform-filter").value;
  const sort = $("sort-filter").value;
  const jobs = state.jobs.filter((job) => {
    const haystack = [job.title, job.company, job.location, job.description].join(" ").toLowerCase();
    return job.status === "active" && job.remote_status === "remote" &&
      (!query || haystack.includes(query)) && (!platform || job.platform === platform);
  });
  jobs.sort((a, b) => {
    const aDate = new Date(sort === "verified" ? a.last_verified_at : a.published_at || a.last_verified_at).getTime() || 0;
    const bDate = new Date(sort === "verified" ? b.last_verified_at : b.published_at || b.last_verified_at).getTime() || 0;
    return bDate - aDate;
  });
  $("job-count").textContent = jobs.length.toLocaleString("ar-EG");
  $("jobs-list").innerHTML = jobs.length ? jobs.map((job) =>
    '<article class="job-card"><div class="job-top"><span class="platform">' + escapeHtml(job.platform) +
    '</span><span class="remote-label">عن بُعد</span></div><h3>' + escapeHtml(job.title) +
    '</h3><p class="company">' + escapeHtml(job.company) + '</p><p class="location">' +
    escapeHtml(job.location || "الموقع غير محدد") + '</p>' +
    (job.source_credit ? '<p class="source-credit">مصدر البيانات: <a href="' + safeHref(job.source_credit_url) + '" target="_blank" rel="noopener noreferrer">Himalayas ↗</a></p>' : '') +
    (job.salary_min != null || job.salary_max != null ? '<p class="salary">' + escapeHtml(job.salary_currency || "") + ' ' + escapeHtml(job.salary_min ?? "—") + ' – ' + escapeHtml(job.salary_max ?? "—") + ' / ' + escapeHtml(job.salary_period || "period not stated") + '</p>' : '') +
    (job.employment_type ? '<p class="job-type">' + escapeHtml(job.employment_type) + '</p>' : '') +
    '<p class="description">' +
    escapeHtml((job.description || "").slice(0, 220)) + ((job.description || "").length > 220 ? "…" : "") +
    '</p><div class="job-meta"><span>النشر: ' + dateLabel(job.published_at) +
    '</span><span>آخر تحقق: ' + dateLabel(job.last_verified_at) +
    '</span></div><a class="button primary apply-link" href="' + safeHref(job.application_url) +
    '" target="_blank" rel="noopener noreferrer">التقديم على المصدر الأصلي ↗</a></article>'
  ).join("") : '<div class="empty">لا توجد فرص مطابقة حالياً. جرّب تغيير كلمات البحث أو عد لاحقاً بعد تحديث المصادر.</div>';
}
async function loadJobs() {
  try {
    const response = await fetch("jobs.json", { cache: "no-store" });
    if (!response.ok) throw new Error("feed unavailable");
    const feed = await response.json();
    state.jobs = Array.isArray(feed.jobs) ? feed.jobs : [];
    const active = state.jobs.filter((job) => job.status === "active" && job.remote_status === "remote");
    const generated = feed.generated_at ? new Date(feed.generated_at) : null;
    const stale = !generated || Number.isNaN(generated.getTime()) || Date.now() - generated.getTime() > 24 * 60 * 60 * 1000;
    $("feed-status").textContent = stale ? "تحديث البيانات غير متاح أو أقدم من 24 ساعة" : "آخر تحديث: " + dateLabel(feed.generated_at);
    $("freshness").hidden = !stale;
    $("freshness").textContent = "تنبيه: لم يتم تحديث موجز الوظائف خلال آخر 24 ساعة. تحقق من المصدر الأصلي قبل الاعتماد على أي إعلان.";
    if (!active.length && feed.notice) $("feed-status").textContent = "لم تُفعّل مصادر وظائف موثقة بعد.";
    renderJobs();
  } catch {
    $("feed-status").textContent = "تعذر تحميل الوظائف";
    $("jobs-list").innerHTML = '<div class="empty">تعذر تحميل البيانات. حاول لاحقاً.</div>';
  }
}
function generateProfile(form) {
  const data = new FormData(form);
  const role = String(data.get("role") || "").trim();
  const skills = String(data.get("skills") || "").split(",").map((x) => x.trim()).filter(Boolean);
  const experience = String(data.get("experience") || "").trim();
  const projects = String(data.get("projects") || "").split("\n").map((x) => x.trim()).filter(Boolean);
  const education = String(data.get("education") || "").trim();
  const languages = String(data.get("languages") || "").split(",").map((x) => x.trim()).filter(Boolean);
  const headline = [role, ...skills.slice(0, 3)].filter(Boolean).join(" | ");
  const paragraphs = [];
  if (role) paragraphs.push("I am building my professional profile for " + role + " opportunities.");
  if (experience) paragraphs.push(experience.endsWith(".") ? experience : experience + ".");
  if (projects.length) paragraphs.push("Selected projects: " + projects.slice(0, 5).join("; ") + ".");
  if (education) paragraphs.push("Education: " + education + ".");
  if (languages.length) paragraphs.push("Languages: " + languages.join(", ") + ".");
  if (!paragraphs.length) paragraphs.push("Add your real role, skills, projects, education, or experience. No qualifications have been assumed.");
  const about = paragraphs.join(" ") + " Please verify every detail before publishing.";
  state.profileText = "PROFESSIONAL HEADLINE\n" + (headline || "Add a target role or real skills") +
    "\n\nPROFILE OVERVIEW\n" + about + "\n\nSKILLS\n" + (skills.join(", ") || "Add your actual skills") +
    "\n\nPROJECTS\n" + (projects.join("\n") || "Add projects you personally completed") +
    "\n\nNOTE\nGenerated only from the information you entered. Review every statement and the platform's field limits before publishing.";
  $("profile-result").innerHTML = '<h4>العنوان المهني</h4><p>' + escapeHtml(headline || "أضف المجال أو المهارات الفعلية") +
    '</p><h4>النبذة</h4><p>' + escapeHtml(about) + '</p><h4>المهارات</h4><p>' +
    escapeHtml(skills.join("، ") || "لم تتم إضافة مهارات") + '</p><h4>المشروعات</h4><p>' +
    escapeHtml(projects.join("؛ ") || "لم تتم إضافة مشروعات") +
    '</p><p class="muted">تم إنشاء النص محلياً في المتصفح. لا تتم إضافة خبرات أو مؤهلات غير مدخلة.</p>';
  $("copy-profile").disabled = false;
}
$("profile-form").addEventListener("submit", (event) => {
  event.preventDefault();
  generateProfile(event.currentTarget);
});
$("copy-profile").addEventListener("click", async () => {
  if (!state.profileText) return;
  const button = $("copy-profile");
  try { await navigator.clipboard.writeText(state.profileText); button.textContent = "تم النسخ"; }
  catch { button.textContent = "تعذر النسخ من المتصفح"; }
});
["search", "platform-filter", "sort-filter"].forEach((id) => $(id).addEventListener("input", renderJobs));
loadJobs();
