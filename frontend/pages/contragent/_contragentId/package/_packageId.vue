<template lang="pug">
  v-row(
    class="fill-height"
    justify="center"
    align="start"
    no-gutters
  )
    v-col(
      xs12
      sm8
      md6
    )
      v-card(
        flat
        exact
      )
        v-toolbar(elevation="0")
          v-btn(
            icon
            :to="'/contragent/' + $route.params.contragentId"
          )
            v-icon mdi-arrow-left
          v-toolbar-title(class="headline font-weight-light") Пакет № {{ package.id }}
          v-spacer
          v-chip(
            outlined
            class="mr-2"
            :color="package.package_state ? 'primary' : 'error'"
          )
            span {{ package.package_state.name_state }}
          comments(view-state="package")
          v-menu(
            v-if="packageActiveStatus"
          )
            template(v-slot:activator="{ on }")
              v-btn(
                icon
                v-on="on"
              )
                v-icon mdi-dots-vertical
            v-list
              v-list-item(
                class="px-0"
                v-for="(event, i) in package.package_state.events"
                :key="i"
              )
                v-btn(
                  text
                  tile
                  block
                  class="custom-transform-class text-none"
                  @click="SEND_EVENT({ contragentId: package.contragent, packageId: package.id, eventId: event.id })"
                )
                  span {{ event.name_event }}
              v-list-item(
                class="px-0"
              )
                v-btn(
                  text
                  tile
                  block
                  class="custom-transform-class text-none"
                  color="primary"
                  @click="REGENERATE_PACKAGE({ contragentId: package.contragent, packageId: package.id })"
                )
                  span Перегенерировать
              v-list-item(
                class="px-0"
              )
                v-btn(
                  text
                  tile
                  block
                  class="custom-transform-class text-none mr-2"
                  color="primary"
                  @click="DOWNLOAD_PACKAGE({ contragentId: package.contragent, packageId: package.id })"
                )
                  span Скачать пакет
                  v-icon(small class="ml-2") mdi-download
        v-tabs(
          v-model="tab"
          background-color="transparent"
          color="primary"
          show-arrows
          grow
        )
          v-tab(
            v-for="item in items"
            :key="item"
          )
            | {{ item }}
        v-tabs-items(v-model="tab")
          v-tab-item
            v-card(
              flat
            )
              v-data-table(
                :headers="headers"
                :items="package.single_files"
                :items-per-page="5"
                class="elevation-0"
              )
                template(v-slot:item.actions="{ item }")
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on }")
                      v-btn(
                        icon
                        v-on="on"
                        color="blue"
                        :href="item.file_path || ''"
                        target="_blank"
                      )
                        v-icon(small) mdi-download
                    span Скачать
          v-tab-item
            v-card(
              flat
            )
              v-data-table(
                :headers="headers"
                :items="package.pack_files['Акт']"
                :items-per-page="5"
                class="elevation-0"
              )
                template(v-slot:item.actions="{ item }")
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on }")
                      v-btn(
                        icon
                        v-on="on"
                        color="blue"
                        :href="item.file_path || ''"
                        target="_blank"
                      )
                        v-icon(small) mdi-download
                    span Скачать
          v-tab-item
            v-card(
              flat
            )
              v-data-table(
                :headers="headers"
                :items="package.pack_files['Счет']"
                :items-per-page="5"
                class="elevation-0"
              )
                template(v-slot:item.actions="{ item }")
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on }")
                      v-btn(
                        icon
                        v-on="on"
                        color="blue"
                        :href="item.file_path || ''"
                        target="_blank"
                      )
                        v-icon(small) mdi-download
                    span Скачать
          v-tab-item
            v-card(
              flat
            )
              v-data-table(
                :headers="headers"
                :items="package.pack_files['Счет-фактура']"
                :items-per-page="5"
                class="elevation-0"
              )
                template(v-slot:item.actions="{ item }")
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on }")
                      v-btn(
                        icon
                        v-on="on"
                        color="blue"
                        :href="item.file_path || ''"
                        target="_blank"
                      )
                        v-icon(small) mdi-download
                    span Скачать
          v-tab-item
            v-card(
              flat
            )
              v-data-table(
                :headers="headers"
                :items="otherFiles"
                :items-per-page="-1"
                class="elevation-0"
                hide-default-footer
              )
                template(v-slot:footer)
                  v-toolbar(flat color="white")
                    v-spacer
                    v-dialog(
                      v-model="packageDialogState"
                      persistent
                      max-width="600px"
                    )
                      template(v-slot:activator="{ on }")
                        v-btn(
                          text
                          tile
                          outlined
                          class="ml-2 custom-transform-class text-none"
                          color="primary"
                          v-on="on"
                        )
                          | Добавить файл
                      v-card(outlined)
                        v-card-title
                          span(class="headline") Добавление файла
                        v-card-text
                          v-container(px-0 pb-0)
                            v-row(no-gutters)
                              v-col(cols="12")
                                VueFileAgent(
                                  ref="vueFileAgent"
                                  v-model="filesDataForUpload"
                                  :theme="'list'"
                                  :maxFiles="1"
                                  :multiple="true"
                                  :deletable="true"
                                  :compact="true"
                                  :helpText="'Загрузите свой файл'"
                                  :errorText="{ type: 'Некоректный тип файла. Доступно только xlsx', size: 'Размер файла выше 2MB' }"
                                  @delete="fileDeleted($event)"
                                )
                                small *Файл должен быть с расширением .xlsx и размером меньше двух мегабайт
                        v-card-actions
                          v-spacer
                          v-btn(color="blue darken-1" text @click="packageDialogState = false") Закрыть
                          v-btn(color="blue darken-1" text @click="upload") Отправить
                template(v-slot:item.actions="{ item }")
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on }")
                      v-btn(
                        icon
                        v-on="on"
                        color="blue"
                        :href="item.file_path || ''"
                        target="_blank"
                      )
                        v-icon(small) mdi-download
                    span Скачать
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on: tooltip }")
                      v-btn(
                        icon
                        v-on="tooltip"
                        @click.stop="openPackageFileWarningDialog(item)"
                        color="red"
                      )
                        v-icon(small) mdi-close
                    span Удалить
                  v-tooltip(bottom)
                    template(v-slot:activator="{ on: tooltip }")
                      comments(
                        v-on="tooltip"
                        view-state="file"
                        :file-id="item.id"
                      )
                        v-icon(small) mdi-close
                    span Коментарии
          v-tab-item
            v-card(
              flat
            )
              v-card-title
              v-card-text
                contragent-act
                tax-count
              v-card-actions
                v-btn(text @click="update") Сохранить
      v-dialog(v-model="packageFileWarningDialog" max-width="360")
        v-card
          v-card-title(class="headline") Удалить выбранный файл?
          v-card-actions
            v-spacer
            v-btn(color="green darken-1" text @click="closePackageFileWarningDialog") Отменить
            v-btn(color="green darken-1" text @click="deleteFile") Удалить
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { ValidationProvider, ValidationObserver } from 'vee-validate'
import comments from '~/components/Comments.vue'
import taxCount from '~/components/packages/packageTaxCount'

import contragentAct from '@/components/contragents/contragentAct'

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
    comments,
    taxCount,
    contragentAct
  },
  async asyncData ({ $axios, store, params }) {
    await store.dispatch('packages/FETCH_PACKAGE', { contragentId: params.contragentId, packageId: params.packageId })
    await store.dispatch('files/FETCH_FILES', { contragentId: params.contragentId, packageId: params.packageId })
  },
  data: () => ({
    packageDialogState: false,
    packageFileWarningDialog: false,
    filesDataForUpload: null,
    currentItemId: null,
    tab: null,
    headers: [
      {
        text: 'Номер',
        align: 'center',
        sortable: false,
        value: 'id'
      },
      { text: 'Имя', value: 'file_name' },
      { text: 'Дата создания', value: 'creation_date' },
      { text: 'Действия', value: 'actions', align: 'center', sortable: false }
      // Дата последнего платежа
      // Ответственное лицо
    ],
    items: [
      'Основные файлы', 'Акты', 'Счета', 'Счета фактур', 'Другие файлы', 'Дополнительная информация'
    ],
    menu: [
      { icon: 'home', title: 'Link A' },
      { icon: 'info', title: 'Link B' },
      { icon: 'warning', title: 'Link C' }
    ]
  }),
  computed: {
    ...mapState({
      package: state => state.packages.detail,
      packageActiveStatus: state => state.packages.detail.is_active,
      otherFiles: state => state.files.list
    })
  },
  methods: {
    ...mapActions({
      REGENERATE_PACKAGE: 'packages/REGENERATE_PACKAGE',
      SEND_EVENT: 'packages/SEND_EVENT',
      DOWNLOAD_PACKAGE: 'packages/DOWNLOAD_PACKAGE',
      DELETE_FILE: 'files/DELETE_FILE',
      UPDATE_PACKAGE: 'packages/UPDATE_PACKAGE'
    }),
    upload () {
      this.$store.dispatch('files/CREATE_FILE', {
        vueFileAgent: this.$refs.vueFileAgent,
        contragentId: this.$route.params.contragentId,
        packageId: this.$route.params.packageId,
        filesDataForUpload: this.filesDataForUpload
      })
      this.packageDialogState = false
      this.filesDataForUpload = null
    },
    update () {
      this.UPDATE_PACKAGE({
        contragentId: this.$route.params.contragentId,
        packageId: this.$route.params.packageId
      })
    },
    deleteFile () {
      this.DELETE_FILE({
        contragentId: this.$route.params.contragentId,
        packageId: this.$route.params.packageId,
        fileId: this.currentItemId
      })
      this.closePackageFileWarningDialog()
      this.currentItemId = null
    },
    fileDeleted (fileData) {
      this.filesDataForUpload = null
    },
    closePackageFileWarningDialog () {
      this.packageFileWarningDialog = false
    },
    openPackageFileWarningDialog (item) {
      this.packageFileWarningDialog = true
      this.currentItemId = item.id
    }
  }
}
</script>
