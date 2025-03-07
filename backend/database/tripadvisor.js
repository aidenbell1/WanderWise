const playwright = require('playwright');
const fs = require('fs');

async function autoScroll(page) {
    await page.evaluate(async () => {
        await new Promise((resolve) => {
            let totalHeight = 0;
            const distance = 500;
            const timer = setInterval(() => {
                const scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if (totalHeight >= scrollHeight) {
                    clearInterval(timer);
                    resolve();
                }
            }, 500);
        });
    });
}

(async () => {
    const browser = await playwright.chromium.launch({ headless: false });
    const context = await browser.newContext();
    const page = await context.newPage();

    const url = "https://www.tripadvisor.com/Attraction_Review-g187147-d188151-Reviews-Eiffel_Tower-Paris_Ile_de_France.html";
    await page.goto(url, { waitUntil: 'networkidle' });

    // Scroll down to load all reviews
    await autoScroll(page);

    // Wait for reviews to appear
    await page.waitForSelector('div[data-automation="reviewCard"]', { timeout: 30000 });

    // Extract reviews
    const reviews = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('div[data-automation="reviewCard"]')).map(review => {
            // Username
            const usernameElement = review.querySelector('span[class*="fiohW"] a');
            const username = usernameElement ? usernameElement.textContent.trim() : "NOT FOUND";
    
            // Rating
            const ratingElement = review.querySelector('svg[class*="UctUV"]');
            const rating = ratingElement ? ratingElement.getAttribute('aria-labelledby') : null; // Extract rating
    
            // Review Title
            const titleElement = review.querySelector('div[class*="qWPrE"] span.yCeTE');
            const title = titleElement ? titleElement.textContent.trim() : "No Title";
    
            // Review Text
            const reviewTextElement = review.querySelector('div[class*="pZUbB"] span.yCeTE');
            const reviewText = reviewTextElement ? reviewTextElement.textContent.trim() : "No Review Text";
    
            // Review Date
            const dateElement = review.querySelector('div[class*="TreSq"] div[class*="osNWb"]');
            const date = dateElement ? dateElement.textContent.trim() : "No Date";
    
            return { username, rating, title, reviewText, date };
        });
    });
    
    fs.writeFileSync('tripadvisor_reviews.json', JSON.stringify(reviews, null, 2));
    console.log('Reviews saved to tripadvisor_reviews.json');

    await browser.close();
})();
