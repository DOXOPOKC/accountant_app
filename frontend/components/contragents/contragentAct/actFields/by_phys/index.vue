<template lang="pug">
  v-col(cols="12")
    v-checkbox(
      v-model="actPhys"
      label="- обращение физических лиц "
    )
    v-text-field(
      v-if="actPhys"
      v-model="actPhysData"
    )
</template>

<script>
export default {
  name: '',
  data: () => ({}),
  computed: {
    actPhys: {
      set (actPhys) {
        this.$store.commit('act/SET_ACT', { by_phys: actPhys })
      },
      get () {
        return this.$store.state.act.detail.by_phys
      }
    },
    actPhysData: {
      set (actPhysData) {
        this.$store.commit('act/SET_ACT', { phys_data: actPhysData })
      },
      get () {
        return this.$store.state.act.detail.phys_data
      }
    }
  }
}
</script>
