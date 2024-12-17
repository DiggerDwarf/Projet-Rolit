from typing import Tuple, Optional, Union, List

__fltk__ = None

def init(fltk) -> None:
    """
    Initialise le module fltk_addons
    """
    global __fltk__
    __fltk__ = fltk

def recuperer_tags(identifiant: int) -> Tuple[str, ...]:
    """
    Renvoie les tags d'un objet
    
    :param identifiant: identifiant de l'objet
    
    :return tags: Tuple contenant les tags de l'objet. Peut être vide.
    """
    assert __fltk__.__canevas is not None
    assert isinstance(identifiant, int)
    return __fltk__.__canevas.canvas.gettags(identifiant)


def liste_objets_survoles() -> Tuple[int, ...]:
    """
    Renvoie l'identifiant de tous les objets actuellement survolés
    """
    assert __fltk__.__canevas is not None
    x, y = __fltk__.abscisse_souris(), __fltk__.ordonnee_souris()
    overlapping = __fltk__.__canevas.canvas.find_overlapping(x, y, x, y)
    return overlapping


def objet_survole() -> Optional[int]:
    """
    Renvoie un objet actuellement survolé
    """
    assert __fltk__.__canevas is not None
    overlapping = liste_objets_survoles()
    if overlapping:
        return overlapping[0]
    return None


def est_objet_survole(objet_ou_tag : Union[int, str, List[str]]) -> bool:
    """
    Renvoie si un objet qui vérifie les conditions d'id ou de tags données est survolé.
    
    Si objet_ou_tag est un int, check si l'objet avec cet identifiant est survolé.
    Si c'est un str, check si un objet avec ce tag l'est
    Si c'est une liste, check si un objet qui remplit toutes ces contraintes l'est
    
    :param objet_ou_tag: Contrainte(s) sur les objets
    """
    assert __fltk__.__canevas is not None
    if isinstance(objet_ou_tag, int):
        return objet_ou_tag in liste_objets_survoles()
    if isinstance(objet_ou_tag, str):
        tags = tuple([objet_ou_tag])
        return any(
            tag_obj in tags for obj in liste_objets_survoles() for tag_obj in recuperer_tags(obj)
        )
    if isinstance(objet_ou_tag, list):
        return all(est_objet_survole(tag) for tag in objet_ou_tag)
    raise TypeError("Argument de type incorrect")


def renomme_fenetre(titre: str) -> None:
    """
    Change le titre de la fenêtre.
    """
    assert __fltk__.__canevas is not None

    __fltk__.__canevas.root.title(titre)