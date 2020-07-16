<template lang="pug">
  v-col(cols="3")
    v-menu(
      ref="menu"
      v-model="menu"
      :close-on-content-click="false"
      :return-value.sync="currentDate"
      transition="scale-transition"
      offset-y
      min-width="290px"
    )
      template(v-slot:activator="{ on }")
        v-text-field(
          dense
          v-model="currentDate"
          label="Конечная дата оказания услуг"
          readonly
          v-on="on"
        )
      v-date-picker(v-model="currentDate" no-title scrollable)
        v-spacer
        v-btn(text color="primary" @click="menu = false") Отмена
        v-btn(text color="primary" @click="$refs.menu.save(currentDate)") OK
</template>

<script>
export default {
  components: {},
  data: () => ({
    menu: false
  }),
  computed: {
    currentDate: {
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
