<template lang="pug">
  v-col(cols="12")
    v-text-field(
      v-model="director_name"
      label="Ответственное лицо"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    director_name: {
      set (directorName) {
        this.$store.commit('contragents/SET_CONTRAGENT', { director_name: directorName })
      },
      get () {
        return this.$store.state.contragents.detail.director_name
      }
    }
  }
}
</script>
