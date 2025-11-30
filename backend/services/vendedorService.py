from backend.DAOs.VendedoresDAO import VendedorDAO
from backend.models.vendedores import Vendedor

class VendedorService:

    @staticmethod
    def obtener_por_id_usuario(id_usuario: int) -> Vendedor | None:
        """
        Obtiene el vendedor asociado al usuario.
        """
        if id_usuario is None:
            print("Id de usuario requerido.")
            return None

        return VendedorDAO.obtener_por_id_usuario(id_usuario)

    @staticmethod
    def registrar_vendedor(id_usuario: int) -> bool:
        """
        Crea un vendedor básico asociado al usuario luego del registro,
        solo si no existe ya uno.
        """
        vendedor_existente = VendedorDAO.obtener_por_id_usuario(id_usuario)
        if vendedor_existente is not None:
            print("Este usuario ya tiene vendedor registrado.")
            return False

        nuevo_vendedor = Vendedor(
            id_usuario=id_usuario,
            nombre_negocio="",
            logo_negocio="",
            descripcion_negocio="",
            es_contribuyente=False
        )

        return VendedorDAO.insertar_vendedor(nuevo_vendedor)

    @staticmethod
    def actualizar_vendedor(vendedor: Vendedor) -> bool:
        """
        Actualiza los datos del vendedor (nombre, logo, descripción, contribuyente)
        """
        if vendedor.id is None:
            print("El vendedor debe tener un ID para actualizar.")
            return False

        return VendedorDAO.actualizar_vendedor(vendedor)
