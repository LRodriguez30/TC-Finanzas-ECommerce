from backend.DAOs.VendedoresDAO import VendedorDAO
from backend.models.vendedores import Vendedor

class VendedorController:

    @staticmethod
    def obtener_vendedor_por_id_usuario(id_usuario: int) -> Vendedor | None:
        """
        Devuelve el vendedor según el IdUsuario asociado.
        """
        return VendedorDAO.obtener_por_id_usuario(id_usuario)

    @staticmethod
    def actualizar_vendedor(vendedor: Vendedor) -> bool:
        """
        Actualiza los datos de un vendedor existente.
        """
        return VendedorDAO.actualizar_vendedor(vendedor)
