import { expect, type Page, test } from "@playwright/test";

const deterministicFonts = `
  :root {
    --sans: "DejaVu Sans", sans-serif !important;
    --mono: "DejaVu Sans Mono", monospace !important;
  }
`;

async function openDocsPage(page: Page, path: string): Promise<void> {
  const response = await page.goto(path, { waitUntil: "networkidle" });
  expect(response?.ok()).toBeTruthy();
  await expect(page.locator("main")).toBeVisible();
  await page.addStyleTag({ content: deterministicFonts });
  await page.evaluate(async () => {
    await document.fonts.ready;
  });
}

async function expectStableScreenshot(
  page: Page,
  name: string,
  fullPage = true,
): Promise<void> {
  await expect(page).toHaveScreenshot(name, {
    animations: "disabled",
    caret: "hide",
    fullPage,
    scale: "css",
    maxDiffPixelRatio: 0.001,
  });
}

test("overview page @desktop", async ({ page }) => {
  await openDocsPage(page, "/index.html");
  await expectStableScreenshot(page, "overview.png");
});

test("lineage DAG @desktop", async ({ page }) => {
  await openDocsPage(page, "/dag.html");
  await expectStableScreenshot(page, "dag.png");
});

test("sync definition and lineage tabs @desktop", async ({ page }) => {
  await openDocsPage(page, "/sync/orders-to-pg.html");
  await expectStableScreenshot(page, "sync-definition.png");

  await page.getByRole("tab", { name: "Lineage" }).click();
  await expect(page.getByRole("tab", { name: "Lineage" })).toHaveAttribute(
    "aria-selected",
    "true",
  );
  await expectStableScreenshot(page, "sync-lineage.png");
});

test("overview page @mobile", async ({ page }) => {
  await openDocsPage(page, "/index.html");
  await expectStableScreenshot(page, "overview.png", false);
});

test("sync definition @mobile", async ({ page }) => {
  await openDocsPage(page, "/sync/orders-to-pg.html");
  await expectStableScreenshot(page, "sync-definition.png", false);
});
