<template lang="pug">
  div.file
    form(enctype="multipart/form-data")
      div.fields
        v-file-input(
          v-model="files"
          color="deep-purple accent-4"
          counter
          label="File input"
          multiple
          placeholder="Select your files"
          prepend-icon="mdi-paperclip"
          outlined
          :show-size="1000"
        )
      div.fields
        button
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { types } from '~/store/contragents'

// const classTypes = [
//     { 0: '' },
//     { 1: 'Юридическое лицо без договора' },
//     { 2: 'Юридическое лицо с договором' },
//     { 3: 'ИЖС без договора' },
//     { 4: 'ИЖС с договором' },
//     { 5: 'Физическое лицо' }
// ]

export default {
  name: 'FileUpload',
  async asyncData ({ $axios, store, params }) {
    await store.dispatch(`contragents/${types.FETCH_CONTRAGENTS}`)
  },
  data: () => ({
    uploaded: false,
    uploadHeaders: {},
    profilePic: null,
    uploadUrl: 'http://localhost/api/contragents/',
    contragentDialogState: false,
    headers: [
      {
        text: 'Название',
        align: 'left',
        sortable: false,
        value: 'excell_name'
      },
      { text: 'Факт. адрес', value: 'physical_address' },
      {
        text: 'Класс',
        value: 'klass'
      },
      { text: 'ИНН', value: 'inn' },
      { text: 'Задолжность', value: 'debt' },
      { text: 'Статус' }
      // Дата последнего платежа
      // Ответственное лицо
    ]
  }),
  computed: {
    ...mapState({
      contragents: state => state.contragents.list
    })
  },
  methods: {
    ...mapActions([types.FETCH_CONTRAGENTS]),
    upload () {
      this.$refs.profilePicRef.upload(this.uploadUrl, this.uploadHeaders, [this.profilePic])
        .then((response) => {
          this.uploaded = true
          setTimeout(() => {
            this.$store.commit('tasks/SET_TASKS', response[0].data)
            this.$store.dispatch('tasks/FETCH_TASKS')
          }, 500)
        })
    },
    onSelect (filesData) {
      this.uploaded = false
    }
  }
}
</script>
