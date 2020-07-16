<template lang="pug">
  v-col(cols="3")
    v-menu(
      ref="menu"
      v-model="menu"
      :close-on-content-click="false"
      :return-value.sync="creationDate"
      transition="scale-transition"
      offset-y
      min-width="290px"
    )
      template(v-slot:activator="{ on }")
        ValidationProvider(rules="" v-slot="{ errors }")
          v-text-field(
            dense
            v-model="creationDate"
            label="Дата создания юр. лица"
            readonly
            v-on="on"
            :error-messages="errors"
          )
      v-date-picker(
        v-model="creationDate"
        no-title
        scrollable
        readonly
      )
        v-spacer
        v-btn(text color="primary" @click="menu = false") Отмена
        v-btn(text color="primary" @click="$refs.menu.save(creationDate)") OK
</template>

<script>
import { ValidationProvider } from 'vee-validate'

export default {
  components: {
    ValidationProvider
  },
  data: () => ({
    menu: false
  }),
  computed: {
    creationDate: {
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
