# 고고다이브 강습 현황 대시보드 — 검사 → 집계 → 암호화 → 깃허브 발행
# 사용:  .\publish.ps1                (비밀번호를 물어봄)
#        .\publish.ps1 -Message "9월 자료 반영"
#        $env:GOGODIVE_DASH_PW = "..." ; .\publish.ps1   (묻지 않음)
param(
    [string]$Password = $env:GOGODIVE_DASH_PW,
    [string]$Message = ""
)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not $Password) {
    $sec = Read-Host "대시보드 비밀번호" -AsSecureString
    $Password = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec))
}
if (-not $Password) { throw "비밀번호가 없습니다." }

Write-Host "1/4 규칙 검사" -ForegroundColor Cyan
python build/test_mapping.py
if (-not $?) { throw "규칙 검사 실패" }

Write-Host "2/4 집계·화면 생성" -ForegroundColor Cyan
python build/build.py
if (-not $?) { throw "빌드 실패 (위 메시지 확인)" }

Write-Host "3/4 암호화" -ForegroundColor Cyan
$env:STATICRYPT_PASSWORD = $Password
npx -y staticrypt@3.5.4 dist/index.html -d . --short --remember 30 --config false `
    --template-title "고고다이브 강습 현황" `
    --template-instructions "운영진 비밀번호를 입력하세요" `
    --template-button "열기" `
    --template-placeholder "비밀번호" `
    --template-remember "이 기기에서 30일간 기억" `
    --template-error "비밀번호가 맞지 않습니다" `
    --template-color-primary "#0F7BA3" `
    --template-color-secondary "#0A2F42"
if (-not $?) { throw "암호화 실패" }
Remove-Item Env:STATICRYPT_PASSWORD

Write-Host "4/4 깃허브 업로드" -ForegroundColor Cyan
$meta = (Get-Content dist/data.json -Raw -Encoding UTF8 | ConvertFrom-Json).meta
if (-not $Message) { $Message = "데이터 $($meta.lastMonth) 까지 반영" }
git add -A
git commit -m $Message
if (-not $?) { Write-Host "커밋할 변경이 없습니다." -ForegroundColor Yellow }
git push
Write-Host "완료: https://gogodive19-droid.github.io/gogodive-edu-dashboard/  (반영까지 1~2분)" -ForegroundColor Green
