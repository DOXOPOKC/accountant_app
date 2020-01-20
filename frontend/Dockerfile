FROM node:12.10-alpine

ENV HOST 0.0.0.0

CMD echo fs.inotify.max_user_watches=524288 | tee -a /etc/sysctl.conf && sysctl -p && npm cache clean --force && npm install -f && npm run dev