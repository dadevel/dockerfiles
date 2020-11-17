FROM archlinux:latest
ENV TERM xterm
COPY ./pacman.conf /etc/pacman.conf
COPY ./sudoers /etc/sudoers
COPY ./entrypoint.sh /
ENV USER_ID 1000
ENV GROUP_ID 1000
RUN chmod 440 /etc/sudoers && \
pacman --sync --refresh --sysupgrade --noconfirm sudo && \
groupadd --gid 998 wheel && \
groupadd --gid $GROUP_ID penelope && \
useradd --uid $USER_ID --gid $GROUP_ID --groups wheel --create-home penelope && \
curl --silent --show-error --output ./strap.sh https://blackarch.org/strap.sh && \
chmod 755 ./strap.sh && \
./strap.sh && \
rm ./strap.sh && \
find / -type f '(' -name '*.pacnew' -or -name '*.pacsave' ')' -delete 2> /dev/null
WORKDIR /home/penelope
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash", "-i"]

