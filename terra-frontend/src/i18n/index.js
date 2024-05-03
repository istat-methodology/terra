import store from "@/store"
import it from "./it.json"
import en from "./en.json"

export const defaultLocale = store.getters["coreui/language"]

export const languages = {
  it,
  en
}
