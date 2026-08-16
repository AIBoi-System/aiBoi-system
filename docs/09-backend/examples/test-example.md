---
title: "Exemplo de teste"
type: tutorial
status: active
owner: quality
canonical: true
ai_index: true
last_verified: 2026-07-16
---

# Exemplo de teste

```python
def test_user_cannot_read_animal_from_another_property(
    client, token_for_user_a, property_b, animal_b
):
    response = client.get(
        f"/animals/{animal_b.id}?property_id={property_b.id}",
        headers={"Authorization": f"Bearer {token_for_user_a}"},
    )

    assert response.status_code == 404
```

Além do caminho feliz, cada CRUD de tenant cobre listagem, leitura, alteração e exclusão cruzadas. Fixtures criam usuários e propriedades independentes e limpam transações com rollback.
