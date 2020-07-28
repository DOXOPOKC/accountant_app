<template lang="pug">
  v-col(cols="12" align="center")
    a(v-if="package.act" :href="package.act.file_path") {{ package.act.file_name }}
    v-dialog(
      v-model="actDialogState"
      max-width="600px"
    )
      template(
        v-slot:activator="{ on }"
      )
        v-btn(
          text small outlined rounded block
          color="primary"
          class=""
          v-on="on"
        ) Заполнить акт
      v-card(
        outlined
      )
        v-card-title Заполните акт
        v-card-text
          v-row(no-gutters)
            v-col(cols="12")
              act-date
              act-time
              act-number
              act-by-plan
              act-by-phys
              act-by-jur
              act-address
              act-exam-descr
              act-evidence
              act-add-info
              act-exam-result
              act-photos
        v-card-actions
          v-spacer
          v-btn(color="blue darken-1" text @click="closeActDialogState") Закрыть
          v-btn(color="blue darken-1" text @click="updateAct") Сохранить
</template>

<script>
import { mapState, mapActions } from 'vuex'

const types = {
  SET_ACT: 'SET_ACT',

  CREATE_ACT: 'CREATE_ACT',
  FETCH_ACT: 'FETCH_ACT'
}

// const date
// const time
// const act_number
// const by_plan
// const by_phys
// const phys_data
// const by_jur
// const jur_data
// const address
// const exam_descr
// const evidence
// const add_info
// const exam_result
// const photos

const actComponents = {
  actDate: () => import('@/components/contragents/contragentAct/actFields/date'),
  actTime: () => import('@/components/contragents/contragentAct/actFields/time'),
  actNumber: () => import('@/components/contragents/contragentAct/actFields/act_number'),
  actByPlan: () => import('@/components/contragents/contragentAct/actFields/by_plan'),
  actByPhys: () => import('@/components/contragents/contragentAct/actFields/by_phys'),
  actByJur: () => import('@/components/contragents/contragentAct/actFields/by_jur'),
  actAddress: () => import('@/components/contragents/contragentAct/actFields/address'),
  actExamDescr: () => import('@/components/contragents/contragentAct/actFields/exam_descr'),
  actEvidence: () => import('@/components/contragents/contragentAct/actFields/evidence'),
  actAddInfo: () => import('@/components/contragents/contragentAct/actFields/add_info'),
  actExamResult: () => import('@/components/contragents/contragentAct/actFields/exam_result'),
  actPhotos: () => import('@/components/contragents/contragentAct/actFields/photos')
}

const actFields = [
  'date',
  'time',
  'act_number',
  'by_plan',
  'by_phys',
  'phys_data',
  'by_jur',
  'jur_data',
  'address',
  'exam_descr',
  'evidence',
  'add_info',
  'exam_result',
  'photos'
]

export default {
  components: actComponents,
  data: () => ({
    actFields,
    actDialogState: false
  }),
  computed: {
    act: {
      set (actValue) {
        this.$store.commit('act/SET_ACT', actValue)
      },
      get () {
        return this.$store.state.act.detail
      }
    },
    ...mapState({
      package: state => state.packages.detail
    })
  },
  methods: {
    ...mapActions('act', [types.CREATE_ACT]),
    closeActDialogState () {
      this.actDialogState = false
    },
    async updateAct () {
      await this.CREATE_ACT({
        contragentId: this.$route.params.contragentId,
        packageId: this.$route.params.packageId
      })
      this.closeActDialogState()
    }
  }
}
</script>
