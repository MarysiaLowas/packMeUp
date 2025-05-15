import { test, expect } from '@playwright/test';

test.describe('Example tests', () => {
  test('homepage has title and content', async ({ page }) => {
    // Navigate to the homepage
    await page.goto('/');
    
    // Verify title contains Pack Me Up
    await expect(page).toHaveTitle(/Pack Me Up/);
    
    // Verify some content is visible
    // Update selector to match actual homepage content
    await expect(page.locator('body')).toBeVisible();
  });
});

// Page Object Model example
class HomePage {
  constructor(private page: any) {}

  async navigate() {
    await this.page.goto('/');
  }

  async getTitle() {
    return this.page.title();
  }
}

test.describe('Page Object Model pattern', () => {
  test('using page object model', async ({ page }) => {
    const homePage = new HomePage(page);
    await homePage.navigate();
    const title = await homePage.getTitle();
    expect(title).toContain('Pack Me Up');
  });
}); 