    @gather_metrics("chat_message")
    def chat_message(
        self,
        name: Literal["user", "assistant", "ai", "human"] | str,
        *,
        avatar: Literal["user", "assistant"] | str | AtomicImage | None = None,
        width: Width = "stretch",
    ) -> DeltaGenerator:
        """Insert a chat message container.

        To add elements to the returned container, you can use ``with`` notation
        (preferred) or just call methods directly on the returned object. See the
        examples below.

        .. note::
            To follow best design practices and maintain a good appearance on
            all screen sizes, don't nest chat message containers.

        Parameters
        ----------
        name : "user", "assistant", "ai", "human", or str
            The name of the message author. Can be "human"/"user" or
            "ai"/"assistant" to enable preset styling and avatars.

            Currently, the name is not shown in the UI but is only set as an
            accessibility label. For accessibility reasons, you should not use
            an empty string.

        avatar : Anything supported by st.image (except list), str, or None
            The avatar shown next to the message.

            If ``avatar`` is ``None`` (default), the icon will be determined
            from ``name`` as follows:

            - If ``name`` is ``"user"`` or ``"human"``, the message will have a
              default user icon.

            - If ``name`` is ``"ai"`` or ``"assistant"``, the message will have
              a default bot icon.

            - For all other values of ``name``, the message will show the first
              letter of the name.

            In addition to the types supported by |st.image|_ (except list),
            the following strings are valid:

            - A single-character emoji. For example, you can set ``avatar="🧑‍💻"``
              or ``avatar="🦖"``. Emoji short codes are not supported.

            - An icon from the Material Symbols library (rounded style) in the
              format ``":material/icon_name:"`` where "icon_name" is the name
              of the icon in snake case.

              For example, ``icon=":material/thumb_up:"`` will display the
              Thumb Up icon. Find additional icons in the `Material Symbols \
              <https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded>`_
              font library.

            - ``"spinner"``: Displays a spinner as an icon.

            .. |st.image| replace:: ``st.image``
            .. _st.image: https://docs.streamlit.io/develop/api-reference/media/st.image

        width : "stretch", "content", or int
            The width of the chat message container. This can be one of the following:

            - ``"stretch"`` (default): The width of the container matches the
              width of the parent container.
            - ``"content"``: The width of the container matches the width of its
              content, but doesn't exceed the width of the parent container.
            - An integer specifying the width in pixels: The container has a
              fixed width. If the specified width is greater than the width of
              the parent container, the width of the container matches the width
              of the parent container.

        Returns
        -------
        Container
            A single container that can hold multiple elements.

        Examples
        --------
        You can use ``with`` notation to insert any element into an expander

        >>> import streamlit as st
        >>> import numpy as np
        >>>
        >>> with st.chat_message("user"):
        ...     st.write("Hello 👋")
        ...     st.line_chart(np.random.randn(30, 3))

        .. output::
            https://doc-chat-message-user.streamlit.app/
            height: 450px

        Or you can just call methods directly in the returned objects:

        >>> import streamlit as st
        >>> import numpy as np
        >>>
        >>> message = st.chat_message("assistant")
        >>> message.write("Hello human")
        >>> message.bar_chart(np.random.randn(30, 3))

        .. output::
            https://doc-chat-message-user1.streamlit.app/
            height: 450px

        """
        if name is None:
            raise StreamlitAPIException(
                "The author name is required for a chat message, please set it via the parameter `name`."
            )

        if avatar is None and (
            name.lower() in {item.value for item in PresetNames} or is_emoji(name)
        ):
            # For selected labels, we are mapping the label to an avatar
            avatar = name.lower()
        avatar_type, converted_avatar = _process_avatar_input(
            avatar, self.dg._get_delta_path_str()
        )

        validate_width(width, allow_content=True)

        message_container_proto = BlockProto.ChatMessage()
        message_container_proto.name = name
        message_container_proto.avatar = converted_avatar
        message_container_proto.avatar_type = avatar_type

        # Set up width configuration
        width_config = WidthConfig()
        if isinstance(width, int):
            width_config.pixel_width = width
        elif width == "content":
            width_config.use_content = True
        else:
            width_config.use_stretch = True

        block_proto = BlockProto()
        block_proto.allow_empty = True
        block_proto.chat_message.CopyFrom(message_container_proto)
        block_proto.width_config.CopyFrom(width_config)

        return self.dg._block(block_proto=block_proto)
