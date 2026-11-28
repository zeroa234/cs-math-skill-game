// Attributes for every box where a number is typed as text (number items, the limit guess). No inputmode:
// iOS has no keypad with digits and a minus sign (UIKit offers none, WebKit bug 193825), so
// inputmode="decimal" left every negative answer untypeable on iPhones (GitHub issue #1), and that pad has
// no / % ^ either for the 3/2, 50%, 2^10 forms that parseNumber reads. The full keyboard has them all.
export const NUMBER_FIELD = { type: "text", autocomplete: "off", spellcheck: false };
