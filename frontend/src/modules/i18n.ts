import { createI18n } from "vue-i18n";
import { messages } from "@/i18n/messages";

// Import i18n resources
// https://vitejs.dev/guide/features.html#glob-import
export const i18n = createI18n({
  legacy: false,
  locale: "en",
  messages,
});
