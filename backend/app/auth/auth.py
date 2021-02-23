from fastapi import APIRouter

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/access-token')
async def login_access():
    """Authenticate user and return ``access_token``, ``refresh_token``

    ---
    Handshake Example:
      - requestBody `content: application/json`
        > schema:
            type: object
            properties:
              username:
                type: string
                required: true
              password:
                type: string
                required: true
      - responses
        - 200 `content: application/json`
          > schema:
              type: object
              properties:
                access_token:
                  type: string
                  example: xx.xx.xx
                refresh_token:
                  type: string
                  example: xx.xx.xx
        - 400
          > description: bad request
    """
    ...

@router.post('/refresh')
async def refresh():
    ...

@router.post('/revoke_access')
async def revoke_access():
    ...

@router.post('/revoke_refresh')
async def revoke_refresh():
    ...
