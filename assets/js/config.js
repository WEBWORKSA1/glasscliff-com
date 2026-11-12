/* Glasscliff.com site configuration — the only file you need to edit for links, prizes and plans. */
window.GC_CONFIG = {
  /* Encoded form-relay key, in two parts (address reversed, then base64). The inbox address never appears in page source. */
  relay: ["bW9jLmxpYW1n", "QDFhc2tyb3diZXc="],
  /* After the first FormSubmit activation email, paste the random alias FormSubmit gives you here (recommended). */
  formAlias: "",
  /* Owner contact for domain / sponsorship / advertising / partnership enquiries. */
  ownerContact: "https://web.works/contact",
  /* Donation and payment links. Paste URLs to switch the Support page from pledge mode to instant checkout.
     e.g. "https://paypal.me/yourname", "https://buy.stripe.com/xxxx", "https://www.buymeacoffee.com/you", "https://ko-fi.com/you" */
  payments: { paypal: "", stripe: "", buymeacoffee: "", kofi: "" },
  /* Edge Prize amounts (first, second, third). */
  prizes: ["US$500 + featured publication", "US$250", "US$100"],
  /* Advisor Network plans (launch rates). */
  advisorPlans: { listed: "US$49 / month", featured: "US$149 / month", referral: "15% of first engagement" },
  /* Reply-time promise shown after submissions. */
  replyTime: "within two business days"
};
