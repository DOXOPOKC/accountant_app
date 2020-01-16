<template lang="pug">
  v-row(
    column
    justify="center"
    align="start"
  )
    v-col(
      xs12
      sm8
      md6
    )
      div(class="text-center")
        logo
        vuetify-logo
      v-card
        v-card-title(class="headline")
          | Welcome to the Vuetify + Nuxt.js template
        v-card-text
          p Vuetify is a progressive Material Design component framework for Vue.js. It was designed to empower developers to create amazing applications.
          p
            |For more information on Vuetify, check out the
            a(href="https://vuetifyjs.com" target="_blank")
              | documentation
            | .
          p Thank you for developing with Vuetify and I look forward to bringing more exciting features in the future.
          div(class="text-xs-right")
            em
              small &mdash; John Leider
          hr(class="my-3")
          a(
            href="https://nuxtjs.org/"
            target="_blank"
          )
            | Nuxt Documentation
          br
          a(
            href="https://github.com/nuxt/nuxt.js"
            target="_blank"
          )
            | Nuxt GitHub
        v-card-actions
          v-spacer
          v-btn(
            color="primary"
            nuxt
            to="/inspire"
          )
            | Continue
</template>

<script>
import Logo from '~/components/Logo.vue'
import VuetifyLogo from '~/components/VuetifyLogo.vue'

export default {
  components: {
    Logo,
    VuetifyLogo
  }
}
</script>
