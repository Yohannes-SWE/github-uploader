import i18n from "i18next"
import { initReactI18next } from "react-i18next"

const resources = {
  en: {
    translation: {
      "Deploy Your Website Globally in Minutes":
        "Deploy Your Website Globally in Minutes",
      "Get Started": "Get Started",
      "Connect GitHub": "Connect GitHub",
      "Connect Render": "Connect Render",
      "Upload Files": "Upload Files",
      "Deploy": "Deploy",
      "Deployment Successful!": "Deployment Successful!",
      "Your website is live at:": "Your website is live at:",
      "Deploy Another Site": "Deploy Another Site",
      "Was this helpful?": "Was this helpful?",
      "Yes": "Yes",
      "No": "No",
      "Thank you for your feedback!": "Thank you for your feedback!",
      "Settings & Profile": "Settings & Profile",
      "Contact Support": "Contact Support",
      "Deployment History": "Deployment History",
      "Export History": "Export History",
      "Import History": "Import History",
      "Loading...": "Loading..."
    }
  },
  es: {
    translation: {
      "Deploy Your Website Globally in Minutes":
        "Despliega tu sitio web globalmente en minutos",
      "Get Started": "Comenzar",
      "Connect GitHub": "Conectar GitHub",
      "Connect Render": "Conectar Render",
      "Upload Files": "Subir archivos",
      "Deploy": "Desplegar",
      "Deployment Successful!": "¡Despliegue exitoso!",
      "Your website is live at:": "Tu sitio web está en:",
      "Deploy Another Site": "Desplegar otro sitio",
      "Was this helpful?": "¿Fue útil esto?",
      "Yes": "Sí",
      "No": "No",
      "Thank you for your feedback!": "¡Gracias por tus comentarios!",
      "Settings & Profile": "Configuración y perfil",
      "Contact Support": "Contactar soporte",
      "Deployment History": "Historial de despliegues",
      "Export History": "Exportar historial",
      "Import History": "Importar historial",
      "Loading...": "Cargando..."
    }
  }
}

i18n.use(initReactI18next).init({
  resources,
  lng: "en",
  fallbackLng: "en",
  interpolation: { escapeValue: false }
})

export default i18n
