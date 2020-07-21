FROM archlinux:latest
ENV TERM xterm
COPY ./pacman.conf /etc/pacman.conf
RUN pacman --sync --refresh --sysupgrade --noconfirm sudo && \
curl --silent --show-error --output ./strap.sh https://blackarch.org/strap.sh && \
chmod 755 ./strap.sh && \
./strap.sh && \
rm ./strap.sh && \
find / -type f '(' -name '*.pacnew' -or -name '*.pacsave' ')' -delete 2> /dev/null
ENV USER_ID 1000
ENV GROUP_ID 1000
COPY ./sudoers /etc/sudoers
RUN chmod 440 /etc/sudoers && \
groupadd --gid $GROUP_ID penelope && \
useradd --uid $USER_ID --gid $GROUP_ID --groups wheel --create-home penelope
WORKDIR /home/penelope
COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash", "-i"]

