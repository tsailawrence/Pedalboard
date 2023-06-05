FROM node:lts
COPY /frontend /frontend
WORKDIR /frontend
RUN npm install -f

# 定義容器啟動時要執行的命令
CMD ["npm", "start"]
EXPOSE 3000