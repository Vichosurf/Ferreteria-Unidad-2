(() => {
    const translations = {
        'Inicio': 'Home',
        'Comprar productos': 'Shop products',
        'Consultas': 'Questions',
        'Historial': 'History',
        'Notificaciones': 'Notifications',
        'Navegación principal': 'Main navigation',
        'Opciones principales': 'Main options',
        'Administración': 'Administration',
        'Cerrar sesión': 'Log out',
        'Iniciar sesión': 'Log in',
        'Crear cuenta': 'Create account',
        'Acceso administrador': 'Admin access',
        'Configuración': 'Settings',
        'Inicio | Ferretería': 'Home | Hardware Store',
        'Catálogo | Ferretería': 'Catalog | Hardware Store',
        'Consulta enviada | Ferretería': 'Question sent | Hardware Store',
        'Enviar consulta | Ferretería': 'Send a question | Hardware Store',
        'Iniciar sesión | Ferretería': 'Log in | Hardware Store',
        'Crear cuenta | Ferretería': 'Create account | Hardware Store',
        'Historial | Ferretería': 'History | Hardware Store',
        'Notificaciones | Ferretería': 'Notifications | Hardware Store',
        'Configuración | Ferretería': 'Settings | Hardware Store',
        'Catálogo de Ferretería': 'Hardware Store Catalog',
        'Productos para tu próximo proyecto.': 'Products for your next project.',
        'Hora de Santiago:': 'Santiago time:',
        '¿Qué necesitas hacer hoy?': 'What would you like to do today?',
        'Elige una opción para continuar en nuestra ferretería.': 'Choose an option to continue.',
        'Enviar una consulta': 'Send a question',
        'Pregúntanos por un producto o solicita asesoría.': 'Ask about a product or request advice.',
        'Comprar productos': 'Shop products',
        'Revisa el catálogo y registra una compra de demostración.': 'Browse the catalog and place a demo order.',
        'Las compras registradas son demostrativas: no se realizan pagos reales.': 'Purchases are for demonstration only; no real payments are made.',
        'Todo para construir tus ideas': 'Everything to build your ideas',
        'Herramientas, materiales y soluciones para cada proyecto.': 'Tools, materials and solutions for every project.',
        'Pedir asesoría': 'Ask for advice',
        'productos en catálogo': 'products in catalog',
        'productos disponibles': 'available products',
        'unidades en inventario': 'units in stock',
        'Buscar producto': 'Search products',
        'Categoría': 'Category',
        'Todas las categorías': 'All categories',
        'Buscar': 'Search',
        'Limpiar': 'Clear',
        'Producto': 'Product',
        'Precio': 'Price',
        'Stock': 'Stock',
        'Disponibilidad': 'Availability',
        'Disponible': 'In stock',
        'Agotado': 'Out of stock',
        'No encontramos productos con esos filtros.': 'No products match those filters.',
        'Consulta de productos': 'Product question',
        'Cuéntanos qué necesitas y el equipo de la ferretería podrá responderte.': 'Tell us what you need and our team will get back to you.',
        'Enviar consulta': 'Send question',
        'Consulta enviada': 'Question sent',
        'Gracias por escribirnos. Tu consulta quedó registrada.': 'Thanks for contacting us. Your question has been recorded.',
        'Volver al catálogo': 'Back to catalog',
        'Crear cuenta de cliente': 'Create customer account',
        'Regístrate para enviar consultas sobre nuestros productos.': 'Create an account to ask us about our products.',
        'Crear cuenta': 'Create account',
        '¿Ya tienes cuenta?': 'Already have an account?',
        'Regístrate aquí': 'Register here',
        '¿No tienes cuenta?': 'New to the store?',
        'Inicia sesión': 'Log in',
        'Ingresar': 'Sign in',
        'Cantidad': 'Quantity',
        'Comprar (demostración)': 'Buy (demo)',
        'La compra es demostrativa; no se realiza ningún cobro.': 'This is a demo purchase; no payment will be collected.',
        'Para comprar o enviar una consulta, inicia sesión con tu cuenta.': 'Log in to buy or send a question.',
        'Mi historial': 'My history',
        'Compras de demostración': 'Demo purchases',
        'Aún no tienes compras registradas.': 'You have no purchases yet.',
        'Consultas enviadas': 'Questions sent',
        'Aún no has enviado consultas.': 'You have not sent any questions yet.',
        'Notificaciones': 'Notifications',
        'Marcar todas como leídas': 'Mark all as read',
        'No tienes notificaciones todavía.': 'You have no notifications yet.',
        'Configuración': 'Settings',
        'Elige el aspecto y el idioma de esta página. Se guardarán en esta sesión.': 'Choose the page theme and language. Preferences are saved for this session.',
        'Idioma / Language': 'Language',
        'Brillo / Theme': 'Theme',
        'Claro / Light': 'Light',
        'Oscuro / Dark': 'Dark',
        'Recibir notificaciones en esta aplicación': 'Receive in-app notifications',
        'Guardar configuración': 'Save settings',
        'Acceso al administrador Django': 'Django administration',
        'Catálogo de Ferretería ·': 'Hardware Store Catalog ·',
        'Preferencias guardadas.': 'Preferences saved.',
        'Mostrando': 'Showing',
        'Herramientas manuales': 'Hand tools',
        'Herramientas eléctricas': 'Power tools',
        'Fijaciones': 'Fasteners',
        'Pinturas': 'Paint',
        'Electricidad': 'Electrical',
        'Seguridad': 'Safety',
        'Construcción': 'Construction',
        'Jardín': 'Garden',
        'Precio:': 'Price:',
        'Agotado temporalmente': 'Temporarily out of stock',
        'Consultar por este producto': 'Ask about this product',
        'Inicia sesión para consultar': 'Log in to ask a question',
        'Consulta general': 'General question',
        'Nombre de usuario': 'Username',
        'Correo electrónico': 'Email address',
        'Contraseña': 'Password',
        'Confirma la contraseña': 'Confirm password',
        'Tu consulta': 'Your question',
        'Producto de interés (opcional)': 'Product of interest (optional)',
        'Este campo es obligatorio.': 'This field is required.',
        'Ej.: taladro, pintura': 'E.g. drill, paint',
        'Compra de demostración registrada; no se realizó ningún cobro.': 'Demo purchase registered; no payment was collected.',
        'Tu consulta fue recibida correctamente.': 'Your question was received.',
        'Ingresa una cantidad válida.': 'Enter a valid quantity.',
        'La cantidad debe ser al menos 1.': 'Quantity must be at least 1.',
        'El stock cambió y ya no alcanza para esa cantidad. Inténtalo nuevamente.': 'Stock changed and is no longer sufficient. Please try again.'
    };

    const applyTranslations = () => {
        if (document.documentElement.lang !== 'en') return;
        if (translations[document.title]) {
            document.title = translations[document.title];
        }
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walker.nextNode())) {
            const text = node.nodeValue.trim();
            if (translations[text]) {
                node.nodeValue = node.nodeValue.replace(text, translations[text]);
            } else if (/^Mostrando \d+ de \d+ productos\.$/.test(text)) {
                node.nodeValue = node.nodeValue.replace(
                    text,
                    text.replace(/^Mostrando (\d+) de (\d+) productos\.$/, 'Showing $1 of $2 products.'),
                );
            } else if (text.startsWith('Disponible · ')) {
                node.nodeValue = node.nodeValue.replace(
                    text,
                    text.replace(/^Disponible · (\d+) unidades$/, 'In stock · $1 units'),
                );
            } else if (text.startsWith('Compra registrada: ')) {
                node.nodeValue = node.nodeValue.replace(
                    text,
                    text.replace(
                        /^Compra registrada: (\d+) x (.+?)\. Este pedido es de demostración y no tiene pago real\.(.*)$/,
                        'Purchase recorded: $1 x $2. This is a demo order; no real payment was made.$3',
                    ),
                );
            } else if (text.startsWith('Solo quedan ')) {
                node.nodeValue = node.nodeValue.replace(
                    text,
                    text.replace(
                        /^Solo quedan (\d+) unidades de (.+)\.$/,
                        'Only $1 units of $2 remain.',
                    ),
                );
            }
        }
        document.querySelectorAll('input[placeholder], textarea[placeholder]').forEach((field) => {
            if (translations[field.placeholder]) field.placeholder = translations[field.placeholder];
        });
        document.querySelectorAll('[aria-label], [title]').forEach((element) => {
            ['aria-label', 'title'].forEach((attribute) => {
                const value = element.getAttribute(attribute);
                if (value && translations[value]) {
                    element.setAttribute(attribute, translations[value]);
                }
            });
        });
        document.querySelectorAll('option').forEach((option) => {
            if (translations[option.textContent.trim()]) {
                option.textContent = translations[option.textContent.trim()];
            }
        });
    };

    const updateClock = () => {
        const clock = document.getElementById('reloj');
        if (!clock) return;
        const now = new Date();
        clock.dateTime = now.toISOString();
        clock.textContent = new Intl.DateTimeFormat(
            document.documentElement.lang === 'en' ? 'en-CA' : 'es-CL',
            { timeZone: 'America/Santiago', hour: '2-digit', minute: '2-digit', second: '2-digit' },
        ).format(now);
    };

    applyTranslations();
    updateClock();
    window.setInterval(updateClock, 1000);
})();
