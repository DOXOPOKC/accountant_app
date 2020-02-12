<template lang="pug">
  v-col(cols="12")
    v-text-field(
      v-model="director_status"
      label="Должность ответственного лица"
    )
</template>

<script>
export default {
  data: () => ({}),
  computed: {
    director_status: {
      set (directorStatus) {
        this.$store.commit('contragents/SET_CONTRAGENT', { director_status: directorStatus })
      },
      get () {
        return this.$store.state.contragents.detail.director_status
      }
    }
  }
}
</script>
