<template lang="pug">
  v-col(cols="12")
    v-menu(
      ref="menu"
      v-model="menu"
      :close-on-content-click="false"
      :return-value.sync="creation_date"
      transition="scale-transition"
      offset-y
      min-width="290px"
    )
      template(v-slot:activator="{ on }")
        v-text-field(
          v-model="creation_date"
          label="Дата создания юр. лица"
          readonly
          v-on="on"
        )
      v-date-picker(v-model="creation_date" no-title scrollable disabled)
        v-spacer
        v-btn(text color="primary" @click="menu = false") Cancel
        v-btn(text color="primary" @click="$refs.menu.save(creation_date)") OK
</template>

<script>
export default {
  data: () => ({
    menu: false
  }),
  computed: {
    creation_date: {
      set (creationDate) {
        this.$store.commit('contragents/SET_CONTRAGENT', { creation_date: creationDate })
      },
      get () {
        return this.$store.state.contragents.detail.creation_date
      }
    }
  }
}
// disabled
</script>
