<template lang="pug">
  v-dialog(v-model="contragentDialogState" persistent max-width="600px")
    v-card(outlined)
      v-card-title
        span(class="headline") Добавление контрагента
      v-card-text
        v-container(px-0 pb-0)
          v-row(no-gutters)
            v-col(cols="12")
              VueFileAgent(
                class="profile-pic-upload-block"
                ref="profilePicRef"
                v-model="profilePic"
                :theme="'list'"
                :accept="'.xlsx'"
                :maxSize="'2MB'"
                :maxFiles="1"
                :multiple="false"
                :deletable="true"
                :compact="true"
                :helpText="'Загрузите свой файл'"
                :errorText="{ type: 'Некоректный тип файла. Доступно только xlsx', size: 'Размер файла выше 2MB' }"
                @select="onSelect($event)"
              )
              small *Файл должен быть с расширением .xlsx и размером меньше двух мегабайт
      v-card-actions
        v-spacer
        v-btn(color="blue darken-1" text @click="contragentDialogState = false") Закрыть
        v-btn(color="blue darken-1" text @click="upload") Отправить
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { types } from '~/store/contragents'

export default {
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
      const self = this
      this.$refs.profilePicRef.upload(this.uploadUrl, this.uploadHeaders, [this.profilePic]).then(function () {
        self.uploaded = true
        setTimeout(function () {
        }, 500)
      })
    },
    onSelect (filesData) {
      this.uploaded = false
    }
  }
}
</script>
