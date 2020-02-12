<template lang="pug">
  v-col(cols="12")
    v-menu(
      ref="menu"
      v-model="menu"
      :close-on-content-click="false"
      :return-value.sync="current_date"
      transition="scale-transition"
      offset-y
      min-width="290px"
    )
      template(v-slot:activator="{ on }")
        v-text-field(
          v-model="current_date"
          label="Конечная дата оказания услуг"
          readonly
          v-on="on"
        )
      v-date-picker(v-model="current_date" no-title scrollable)
        v-spacer
        v-btn(text color="primary" @click="menu = false") Cancel
        v-btn(text color="primary" @click="$refs.menu.save(current_date)") OK
</template>

<script>
export default {
  components: {},
  data: () => ({
    menu: false
  }),
  computed: {
    current_date: {
      set (currentDate) {
        this.$store.commit('contragents/SET_CONTRAGENT', { current_date: currentDate })
      },
      get () {
        return this.$store.state.contragents.detail.current_date
      }
    }
  }
}
// date picker
</script>
